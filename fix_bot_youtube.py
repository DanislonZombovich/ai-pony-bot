with open("bot.py", "r") as f:
    code = f.read()

yt_exec = """
                elif call.name == "play_youtube":
                    url = call.args.get("url")
                    success = await voice_manager.play_youtube_direct(message.guild, url)
                    if success:
                        final_response += f"\\n*Действие:* Включил видео с YouTube."
                    else:
                        final_response += f"\\n*Действие:* Ошибка воспроизведения YouTube или бот не в голосовом канале."
                elif call.name == "stop_youtube":
                    success = await voice_manager.stop_youtube_direct(message.guild)
                    if success:
                        final_response += "\\n*Действие:* Остановил видео и вернулся к общению."
                    else:
                        final_response += "\\n*Действие:* Сейчас ничего не играет."
"""

import re
code = re.sub(
    r'(elif call.name == "leave_voice":.*?final_response \+= "\\n\*Действие:\* Покинул голосовой канал\.")',
    r'\1\n' + yt_exec.strip(),
    code,
    flags=re.DOTALL
)

with open("bot.py", "w") as f:
    f.write(code)

print("Updated bot.py with youtube execution logic")
