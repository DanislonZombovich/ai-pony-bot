import discord
from discord.ext import commands
import asyncio
from google import genai

from memory import MemoryManager
from ai_core import AICore
from moderation import get_moderation_tools, ModerationHandler
from live_voice import VoiceManager
import bot_settings
import config

DISCORD_TOKEN = config.DISCORD_TOKEN
GEMINI_API_KEY = config.GEMINI_API_KEY
DATABASE_URL = getattr(config, "DATABASE_URL", "") or getattr(config, "AIVEN_URI", "")
ADMIN_ID = config.ADMIN_ID

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

genai_client = genai.Client(api_key=GEMINI_API_KEY)
ai_core = AICore(client=genai_client, model_name=bot_settings.TEXT_MODEL)
voice_manager = VoiceManager(bot, genai_client)

memory_manager = None
memory_store = {}  # Fallback in-memory dictionary if DB is offline

mod_handler = ModerationHandler(bot, ADMIN_ID)
mod_tools = get_moderation_tools()

@bot.event
async def on_ready():
    global memory_manager
    print(f"Logged in as {bot.user}")
    try:
        if DATABASE_URL:
            memory_manager = MemoryManager(DATABASE_URL)
            await memory_manager.connect()
            print("Successfully connected to Neon Serverless PostgreSQL!")
        else:
            print("DATABASE_URL not configured. Using local in-memory fallback.")
    except Exception as e:
        print(f"Failed to connect to Neon PostgreSQL: {e}")
        print("Falling back to local in-memory store...")
        memory_manager = None

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    # Respond only if bot is mentioned or if direct message
    if bot.user not in message.mentions and not isinstance(message.channel, discord.DMChannel):
        await bot.process_commands(message)
        return

    async with message.channel.typing():
        channel_id = message.channel.id
        context_limit = getattr(bot_settings, "CONTEXT_LIMIT", 40)

        if memory_manager:
            context = await memory_manager.get_context(channel_id, limit=context_limit)
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
                call_name = getattr(call, "name", None) or call.get("name")
                call_args = getattr(call, "args", None) or call.get("args") or {}

                if call_name == "join_voice":
                    channel_name = call_args.get("channel_name", "")
                    channel = None

                    if not channel_name or channel_name.lower() in ["текущий", "мой", "тут", "здесь", "current", "here"]:
                        if message.author.voice:
                            channel = message.author.voice.channel

                    if not channel and channel_name:
                        search = channel_name.lower()
                        for c in message.guild.voice_channels:
                            if str(c.id) == search or c.name.lower() == search:
                                channel = c
                                break
                        if not channel:
                            for c in message.guild.voice_channels:
                                if search in c.name.lower():
                                    channel = c
                                    break

                    if channel:
                        success = await voice_manager.join_channel_direct(channel, message.guild)
                        if success:
                            final_response += f"\n*Действие:* Зашел в канал {channel.name}."
                        else:
                            final_response += f"\n*Действие:* Я уже в голосовом канале или произошла ошибка входа в канал {channel.name}."
                    else:
                        if not channel_name:
                            final_response += f"\n*Действие:* Вы не в голосовом канале, и канал не указан."
                        else:
                            final_response += f"\n*Действие:* Канал {channel_name} не найден."

                elif call_name == "leave_voice":
                    await voice_manager.leave_channel_direct(message.guild)
                    final_response += "\n*Действие:* Покинул голосовой канал."

                elif call_name == "play_youtube":
                    url = call_args.get("url")
                    success = await voice_manager.play_youtube_direct(message.guild, url)
                    if success:
                        final_response += f"\n*Действие:* Включил видео с YouTube."
                    else:
                        final_response += f"\n*Действие:* Ошибка воспроизведения YouTube или бот не в голосовом канале."

                elif call_name == "stop_youtube":
                    success = await voice_manager.stop_youtube_direct(message.guild)
                    if success:
                        final_response += "\n*Действие:* Остановил видео и вернулся к общению."
                    else:
                        final_response += "\n*Действие:* Сейчас ничего не играет."

                else:
                    result = await mod_handler.execute_call(call, message.guild, message.author)
                    final_response += f"\n*Действие:* {result}"

        # Persist conversation turn in memory
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

            if len(memory_store[channel_id]) > context_limit:
                memory_store[channel_id] = memory_store[channel_id][-context_limit:]

        if final_response:
            # Discord message size limit is 2000 chars; truncate or split safely
            if len(final_response) <= 2000:
                await message.reply(final_response)
            else:
                for chunk_start in range(0, len(final_response), 1900):
                    await message.reply(final_response[chunk_start:chunk_start + 1900])

    await bot.process_commands(message)

@bot.command()
async def join(ctx):
    await voice_manager.join_channel(ctx)

@bot.command()
async def leave(ctx):
    await voice_manager.leave_channel(ctx)

if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("ERROR: DISCORD_TOKEN is not set in environment or .env file.")
        exit(1)
    bot.run(DISCORD_TOKEN)
