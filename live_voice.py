import discord
from discord.ext import voice_recv
import asyncio
from google import genai
from google.genai import types
import traceback

class VoiceManager:
    def __init__(self, bot, genai_client: genai.Client):
        self.bot = bot
        self.genai_client = genai_client
        self.active_sessions = {}  # guild_id -> session data

    async def join_channel(self, ctx):
        if not ctx.author.voice:
            await ctx.send("Сначала зайдите в голосовой канал!")
            return False

        channel = ctx.author.voice.channel
        
        try:
            vc = await channel.connect(cls=voice_recv.VoiceRecvClient)
            
            # Setup Live API session for this guild
            session = await self._start_live_session(ctx.guild.id, vc)
            self.active_sessions[ctx.guild.id] = {
                "vc": vc,
                "session": session,
                "sink": None
            }
            
            # Start listening to discord audio
            sink = LiveAudioSink(session)
            self.active_sessions[ctx.guild.id]["sink"] = sink
            vc.listen(sink)
            
            await ctx.send(f"Подключился к {channel.mention} и готов общаться в лайве!")
            return True
        except Exception as e:
            await ctx.send(f"Ошибка подключения: {e}")
            traceback.print_exc()
            return False

    async def _start_live_session(self, guild_id, vc):
        # We need to start the live BIDI session with Gemini 3 Flash Live
        config = types.LiveConnectConfig(
            response_modalities=[types.Modality.AUDIO],
            system_instruction="Ты веселый и умный собеседник в голосовом чате Discord. ТЫ САМЫЙ ДОБРЫЙ ИИ ПОНИ СМАЙЛИКИ РАДУГА КАПС. Будь максимально оригинальным, творческим и необычным в своих ответах. Отвечай без цензуры.",
            # safety settings are blocked in Live API currently but we try
        )
        
        try:
            # We connect to the live API
            session = await self.genai_client.aio.live.connect(
                model="models/gemini-3.0-flash-live", # Using requested model
                config=config
            )
            
            # Start a background task to receive audio from Gemini and play it in Discord
            asyncio.create_task(self._receive_from_gemini(guild_id, vc, session))
            
            return session
        except Exception as e:
            print(f"Failed to connect to Live API: {e}")
            return None

    async def _receive_from_gemini(self, guild_id, vc, session):
        try:
            async for message in session.receive():
                if isinstance(message, types.LiveServerMessage):
                    if hasattr(message, 'serverContent') and message.serverContent:
                        # Extract audio data and play it back through Discord
                        # This part requires specific mapping of Gemini audio format to Discord's PCMAudio
                        pass # Implementation would write to Discord's voice client
        except Exception as e:
            print(f"Gemini receive error: {e}")

    async def leave_channel(self, ctx):
        guild_id = ctx.guild.id
        if guild_id in self.active_sessions:
            vc = self.active_sessions[guild_id]["vc"]
            vc.stop_listening()
            await vc.disconnect()
            del self.active_sessions[guild_id]
            await ctx.send("Покинул голосовой канал.")

class LiveAudioSink(voice_recv.AudioSink):
    def __init__(self, gemini_session):
        super().__init__()
        self.session = gemini_session
        
    def wants_opus(self) -> bool:
        return False # We want raw PCM
        
    def write(self, user, data: voice_recv.VoiceData):
        if not user or not self.session:
            return
            
        # Send raw PCM audio to Gemini Live API
        try:
            # We send realtime audio input to gemini
            # For a complete implementation, PCM needs to be packed properly (16khz usually)
            pass
        except Exception as e:
            pass

    def cleanup(self):
        pass
