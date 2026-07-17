# The bot works, let's verify if `live_voice.py` uses `voice_recv` correctly. 
# `discord.AudioSource` reads 3840 bytes per frame (20ms at 48kHz stereo, 16bit = 48000*2*2*0.02 = 3840 bytes). Yes.
# The user wants it to respond in voice channel.
