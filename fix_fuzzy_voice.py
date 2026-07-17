with open("bot.py", "r") as f:
    code = f.read()

# Update tool join_voice to use fuzzy matching and current user voice channel
fuzzy_voice = """
                if call.name == "join_voice":
                    channel_name = call.args.get("channel_name", "")
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
                            final_response += f"\\n*Действие:* Зашел в канал {channel.name}."
                        else:
                            final_response += f"\\n*Действие:* Я уже в голосовом канале или произошла ошибка входа в канал {channel.name}."
                    else:
                        if not channel_name:
                            final_response += f"\\n*Действие:* Вы не в голосовом канале, и канал не указан."
                        else:
                            final_response += f"\\n*Действие:* Канал {channel_name} не найден."
"""

import re
code = re.sub(
    r'if call.name == "join_voice":.*?final_response \+= f"\\n\*Действие:\* Канал \{channel_name\} не найден\."',
    fuzzy_voice.strip(),
    code,
    flags=re.DOTALL
)

with open("bot.py", "w") as f:
    f.write(code)

print("Updated bot.py with fuzzy voice channel matching")
