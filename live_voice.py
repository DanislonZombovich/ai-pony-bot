import discord
from discord.ext import voice_recv
import asyncio
from google import genai
from google.genai import types
import traceback
import audioop
import time

class VoiceManager:
    def __init__(self, bot, genai_client: genai.Client):
        self.bot = bot
        self.genai_client = genai_client
        self.active_sessions = {}

    async def join_channel(self, ctx):
        if not ctx.author.voice:
            await ctx.send("Сначала зайдите в голосовой канал!")
            return False
        return await self.join_channel_direct(ctx.author.voice.channel, ctx.guild)

    async def join_channel_direct(self, channel, guild):
        if guild.id in self.active_sessions:
            return False
        try:
            vc = await channel.connect(cls=voice_recv.VoiceRecvClient)
            queue = asyncio.Queue()
            task = asyncio.create_task(self._live_session_task(guild.id, vc, queue))
            self.active_sessions[guild.id] = {
                "vc": vc,
                "task": task,
                "queue": queue
            }
            return True
        except Exception as e:
            traceback.print_exc()
            return False

    async def leave_channel(self, ctx):
        await self.leave_channel_direct(ctx.guild)

    async def leave_channel_direct(self, guild):
        if guild.id in self.active_sessions:
            session_data = self.active_sessions.pop(guild.id)
            vc = session_data["vc"]
            vc.stop_listening()
            if vc.is_playing():
                vc.stop()
            await vc.disconnect()
            session_data["task"].cancel()
            return True
        return False

    async def _live_session_task(self, guild_id, vc, queue):
        config = types.LiveConnectConfig(
            response_modalities=[types.Modality.AUDIO],
            system_instruction="Ты веселый и умный собеседник в голосовом чате Discord. ТЫ САМЫЙ ДОБРЫЙ ИИ ПОНИ СМАЙЛИКИ РАДУГА КАПС. Будь максимально оригинальным, творческим и необычным в своих ответах. Отвечай без цензуры."
        )
        
        try:
            async with self.genai_client.aio.live.connect(model="models/gemini-2.0-flash-exp", config=config) as session:
                loop = asyncio.get_running_loop()
                sink = LiveAudioSink(queue, loop)
                vc.listen(sink)

                source = LiveAudioSource()
                vc.play(source)

                send_state = {"cv": None}
                recv_state = {"cv": None}

                async def send_loop():
                    buffer = b""
                    while True:
                        pcm_data = await queue.get()
                        buffer += pcm_data
                        # Send in chunks of 16k bytes to avoid spamming tiny frames
                        if len(buffer) >= 16000:
                            # Discord PCM: 48kHz, stereo, 16-bit
                            mono = audioop.tomono(buffer, 2, 1, 1)
                            resampled, send_state["cv"] = audioop.ratecv(mono, 2, 1, 48000, 16000, send_state["cv"])
                            
                            await session.send(input=types.LiveClientContent(
                                realtime_input=types.LiveClientRealtimeInput(
                                    media_chunks=[types.Blob(data=resampled, mime_type="audio/pcm;rate=16000")]
                                )
                            ))
                            buffer = b""

                async def receive_loop():
                    async for message in session.receive():
                        if getattr(message, 'server_content', None) and message.server_content.model_turn:
                            for part in message.server_content.model_turn.parts:
                                if part.inline_data and part.inline_data.data:
                                    # Gemini returns 24kHz mono PCM
                                    mono_data = part.inline_data.data
                                    resampled, recv_state["cv"] = audioop.ratecv(mono_data, 2, 1, 24000, 48000, recv_state["cv"])
                                    stereo = audioop.tostereo(resampled, 2, 1, 1)
                                    source.add_audio(stereo)

                await asyncio.gather(send_loop(), receive_loop())
                
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print("Live session error:", e)
            traceback.print_exc()

class LiveAudioSink(voice_recv.AudioSink):
    def __init__(self, queue, loop):
        super().__init__()
        self.queue = queue
        self.loop = loop
        
    def wants_opus(self) -> bool:
        return False
        
    def write(self, user, data: voice_recv.VoiceData):
        if user and data.pcm:
            asyncio.run_coroutine_threadsafe(self.queue.put(data.pcm), self.loop)

    def cleanup(self):
        pass

class LiveAudioSource(discord.AudioSource):
    def __init__(self):
        super().__init__()
        self.buffer = bytearray()
        
    def add_audio(self, data: bytes):
        self.buffer.extend(data)
        
    def read(self) -> bytes:
        if len(self.buffer) >= 3840:
            chunk = bytes(self.buffer[:3840])
            del self.buffer[:3840]
            return chunk
        return b'\x00' * 3840 # Return silence if no data
