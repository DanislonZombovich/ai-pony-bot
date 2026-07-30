import paramiko

host = "213.176.116.243"
user = "root"
pwd = "L02z14sDNbsC"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username=user, password=pwd)

def run(cmd):
    print(f"Running: {cmd}")
    stdin, stdout, stderr = ssh.exec_command(cmd)
    return stdout.read().decode()

code = run("cat /opt/ai-pony-bot/live_voice.py")

# The user states "у него не работает голос" (voice doesn't work).
# Possible issues:
# 1. Discord PyNaCl or ffmpeg missing (we installed them).
# 2. Resampling logic or chunk sizes might be wrong.
# 3. AudioSink might not be putting data in queue.
# 4. Gemini doesn't respond because audio is silent.
# 5. Model mismatch for Bidi generation.

new_code = code.replace('model="gemini-2.5-flash-native-audio-latest"', f'model="gemini-2.5-flash-native-audio-latest"')

# Let's add some debugging logs into live_voice.py to see what's happening.
debug_code = code.replace(
    'vc = await channel.connect(cls=voice_recv.VoiceRecvClient)',
    'vc = await channel.connect(cls=voice_recv.VoiceRecvClient)\n            print(f"Connected to voice channel: {channel.name}")'
)

debug_code = debug_code.replace(
    'async for message in session.receive():',
    'print("Started receiving from Gemini")\n                    async for message in session.receive():'
)

debug_code = debug_code.replace(
    'source.add_audio(stereo)',
    'source.add_audio(stereo)\n                                    print(f"Added {len(stereo)} bytes of audio to playback source")'
)

debug_code = debug_code.replace(
    'buffer += pcm_data',
    'buffer += pcm_data\n                        if len(buffer) == len(pcm_data): print("Receiving audio from Discord...")'
)

with open("live_voice_updated.py", "w") as f:
    f.write(debug_code)

print("Downloaded and modified live_voice.py")
ssh.close()
