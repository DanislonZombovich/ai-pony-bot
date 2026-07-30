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
    for line in iter(stdout.readline, ""):
        print(line, end="")
    for line in iter(stderr.readline, ""):
        print(line, end="")

with open("live_voice_updated.py", "r") as f:
    content = f.read()
    
# Wait, let's look at how Gemini receives audio.
# Gemini 2.0 Live API expects: {"realtime_input": {"media_chunks": [{"data": b, "mime_type": "audio/pcm;rate=16000"}]}}
# Does audioop.ratecv output correctly? It outputs (fragment, state).
# Is discord.py sending voice_recv data?
# VoiceData.pcm is 16-bit 48kHz stereo.
# audioop.tomono(buffer, 2, 1, 1) averages the two channels.
# Then ratecv from 48000 to 16000.
# All this should work. The issue might be that no one is speaking, so no audio is sent, or Gemini just doesn't reply.

# Let's add text input capabilities to the Live Session so the bot starts the conversation
# When joining, we can send a text turn saying "Привет, я присоединился!"
init_text = """
                # Send an initial greeting
                await session.send(input=types.LiveClientContent(
                    turns=[types.Content(
                        role="user",
                        parts=[types.Part.from_text(text="Я только что присоединился к голосовому каналу. Поздоровайся голосом со всеми!")]
                    )]
                ))
"""
content = content.replace("send_state = {\"cv\": None}", init_text + "\n                send_state = {\"cv\": None}")

cmd_create = f"cat << 'INNER_EOF' > /opt/ai-pony-bot/live_voice.py\n{content}\nINNER_EOF"
run(cmd_create)
ssh.close()
