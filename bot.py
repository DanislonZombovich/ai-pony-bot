import discord
from discord.ext import commands
import asyncio
from google import genai

from memory import MemoryManager
from ai_core import AICore
from moderation import get_moderation_tools, ModerationHandler


import config
DISCORD_TOKEN = config.DISCORD_TOKEN
GEMINI_API_KEY = config.GEMINI_API_KEY
AIVEN_URI = config.AIVEN_URI
ADMIN_ID = config.ADMIN_ID

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

genai_client = genai.Client(api_key=GEMINI_API_KEY)
ai_core = AICore(client=genai_client)

memory_manager = None
memory_store = {} # Fallback dictionary

mod_handler = ModerationHandler(bot, ADMIN_ID)
mod_tools = get_moderation_tools()

@bot.event
async def on_ready():
    global memory_manager
    print(f"Logged in as {bot.user}")
    try:
        if AIVEN_URI:
            memory_manager = MemoryManager(AIVEN_URI)
            await memory_manager.connect()
            print("Successfully connected to Aiven PostgreSQL!")
    except Exception as e:
        print(f"Failed to connect to Aiven PostgreSQL: {e}")
        print("Falling back to local dictionary memory...")
        memory_manager = None

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user not in message.mentions and not isinstance(message.channel, discord.DMChannel):
        await bot.process_commands(message)
        return
        
    async with message.channel.typing():
        channel_id = message.channel.id
        
        if memory_manager:
            context = await memory_manager.get_context(channel_id, limit=40)
        else:
            context = "\n".join(memory_store.get(channel_id, []))
        
        prompt = message.content.replace(f"<@{bot.user.id}>", "").strip()
        
        response_text, function_calls = await ai_core.generate_response(
            prompt=prompt,
            attachments=message.attachments,
            context=context,
            tools=[mod_tools]
        )
        
        final_response = response_text or ""
        
        if function_calls:
            for call in function_calls:
                result = await mod_handler.execute_call(call, message.guild, message.author)
                final_response += f"\n*Действие:* {result}"
        
        if memory_manager:
            await memory_manager.add_message(channel_id, message.author.id, message.author.name, prompt, is_bot=False)
            if final_response:
                await memory_manager.add_message(channel_id, bot.user.id, "Bot", final_response, is_bot=True)
        else:
            if channel_id not in memory_store:
                memory_store[channel_id] = []
                
            memory_store[channel_id].append(f"{message.author.name}: {prompt}")
            if final_response:
                memory_store[channel_id].append(f"Bot: {final_response}")
            
            if len(memory_store[channel_id]) > 40:
                memory_store[channel_id] = memory_store[channel_id][-40:]
            
        if final_response:
            await message.reply(final_response)
        
    await bot.process_commands(message)

from live_voice import VoiceManager
voice_manager = VoiceManager(bot, genai_client)

@bot.command()
async def join(ctx):
    await voice_manager.join_channel(ctx)

@bot.command()
async def leave(ctx):
    await voice_manager.leave_channel(ctx)

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
