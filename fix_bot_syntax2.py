with open("bot.py", "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.startswith('elif call.name == "play_youtube":'):
        new_lines.append('                ' + line)
    else:
        new_lines.append(line)

code = "".join(new_lines)
code = code.replace('final_response += "\n*Действие:* Остановил видео и вернулся к общению."', 'final_response += "\\n*Действие:* Остановил видео и вернулся к общению."')
code = code.replace('final_response += "\n*Действие:* Сейчас ничего не играет."', 'final_response += "\\n*Действие:* Сейчас ничего не играет."')

with open("bot.py", "w") as f:
    f.write(code)
