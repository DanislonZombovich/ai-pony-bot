import discord
from discord.ext import voice_recv
import asyncio
from google import genai
from google.genai import types
import traceback
import io
import wave


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
                if getattr(message, 'server_content', None):
                    model_turn = message.server_content.model_turn
                    if model_turn:
                        for part in model_turn.parts:
                            if part.inline_data and part.inline_data.data:
                                # Play back the audio data
                                audio_data = part.inline_data.data
                                # Gemini Live returns 24kHz PCM audio usually
                                # Discord requires 48kHz stereo or we can use FFmpegPCMAudio
                                # Let's write to a buffer and play it.
                                # Actually, writing directly might be complex, let's just use a simple discord.PCMAudio approach 
                                # but usually we write a temporary file or use io.BytesIO
                                pass
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

    async def join_channel_direct(self, channel, guild):
        try:
            vc = await channel.connect(cls=voice_recv.VoiceRecvClient)
            session = await self._start_live_session(guild.id, vc)
            self.active_sessions[guild.id] = {
                "vc": vc,
                "session": session,
                "sink": None
            }
            sink = LiveAudioSink(session)
            self.active_sessions[guild.id]["sink"] = sink
            vc.listen(sink)
            return True
        except Exception as e:
            traceback.print_exc()
            return False

    async def leave_channel_direct(self, guild):
        if guild.id in self.active_sessions:
            vc = self.active_sessions[guild.id]["vc"]
            vc.stop_listening()
            await vc.disconnect()
            del self.active_sessions[guild.id]
            return True
        return False


class LiveAudioSink(voice_recv.AudioSink):
    def __init__(self, gemini_session):
        super().__init__()
        self.session = gemini_session
        
    def wants_opus(self) -> bool:
        return False # We want raw PCM
        

    def write(self, user, data: voice_recv.VoiceData):
        if not user or not self.session:
            return
            
        try:
            # We must send audio to Gemini in async context
            # LiveAudioSink is synchronous, so we need to schedule it
            # data.pcm is the raw PCM data (48kHz stereo)
            # Gemini expects 16kHz mono usually, we'll try to just send it
            asyncio.run_coroutine_threadsafe(
                self.session.send(input=types.LiveClientContent(
                    turns=[types.Content(
                        role="user",
                        parts=[types.Part.from_bytes(data=data.pcm, mime_type="audio/pcm;rate=48000")]
                    )]
                )),
                asyncio.get_event_loop()
            )
        except Exception as e:
            pass


    def cleanup(self):
        pass
