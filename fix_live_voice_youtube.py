with open("live_voice.py", "r") as f:
    code = f.read()

import_add = """import yt_dlp
import os
"""
code = code.replace("import audioop\nimport time", "import audioop\nimport time\n" + import_add)

yt_logic = """
    async def play_youtube_direct(self, guild, url):
        if guild.id not in self.active_sessions:
            return False
            
        session_data = self.active_sessions[guild.id]
        vc = session_data["vc"]
        
        # Stop current playback
        if vc.is_playing():
            vc.stop()
            
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': f'%(id)s_{guild.id}.%(ext)s',
            'quiet': True,
            'no_warnings': True
        }
        
        try:
            loop = asyncio.get_event_loop()
            def extract():
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    url2 = info['url']
                    return url2
                    
            url2 = await loop.run_in_executor(None, extract)
            
            FFMPEG_OPTIONS = {
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                'options': '-vn'
            }
            
            source = discord.FFmpegPCMAudio(url2, **FFMPEG_OPTIONS)
            vc.play(source)
            session_data["playing_yt"] = True
            return True
        except Exception as e:
            traceback.print_exc()
            return False

    async def stop_youtube_direct(self, guild):
        if guild.id not in self.active_sessions:
            return False
            
        session_data = self.active_sessions[guild.id]
        if not session_data.get("playing_yt"):
            return False
            
        vc = session_data["vc"]
        if vc.is_playing():
            vc.stop()
            
        # Resume AI Live playback source
        source = LiveAudioSource()
        session_data["source"] = source
        vc.play(source)
        session_data["playing_yt"] = False
        return True
"""

# inject after leave_channel_direct
code = code.replace(
"""        return False

    async def _live_session_task(self, guild_id, vc, queue):""",
"""        return False

""" + yt_logic + """

    async def _live_session_task(self, guild_id, vc, queue):"""
)

# Replace source assignment to keep track of it
code = code.replace(
"""                source = LiveAudioSource()
                vc.play(source)""",
"""                source = LiveAudioSource()
                self.active_sessions[guild_id]["source"] = source
                vc.play(source)"""
)

# Avoid writing to source if yt is playing
code = code.replace(
"""                                    stereo = audioop.tostereo(resampled, 2, 1, 1)
                                    source.add_audio(stereo)""",
"""                                    stereo = audioop.tostereo(resampled, 2, 1, 1)
                                    if guild_id in self.active_sessions and not self.active_sessions[guild_id].get("playing_yt"):
                                        self.active_sessions[guild_id]["source"].add_audio(stereo)"""
)

with open("live_voice.py", "w") as f:
    f.write(code)

print("Updated live_voice.py with youtube logic")
