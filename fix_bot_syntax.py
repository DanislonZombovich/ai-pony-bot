with open("bot.py", "r") as f:
    code = f.read()

# Fix broken strings caused by raw \n replacement
code = code.replace('final_response += f"\n*Действие:* Зашел в канал {channel.name}."', 'final_response += f"\\n*Действие:* Зашел в канал {channel.name}."')
code = code.replace('final_response += f"\n*Действие:* Я уже в голосовом канале или произошла ошибка входа в канал {channel.name}."', 'final_response += f"\\n*Действие:* Я уже в голосовом канале или произошла ошибка входа в канал {channel.name}."')
code = code.replace('final_response += f"\n*Действие:* Вы не в голосовом канале, и канал не указан."', 'final_response += f"\\n*Действие:* Вы не в голосовом канале, и канал не указан."')
code = code.replace('final_response += f"\n*Действие:* Канал {channel_name} не найден."', 'final_response += f"\\n*Действие:* Канал {channel_name} не найден."')

code = code.replace('final_response += f"\n*Действие:* Включил видео с YouTube."', 'final_response += f"\\n*Действие:* Включил видео с YouTube."')
code = code.replace('final_response += f"\n*Действие:* Ошибка воспроизведения YouTube или бот не в голосовом канале."', 'final_response += f"\\n*Действие:* Ошибка воспроизведения YouTube или бот не в голосовом канале."')

with open("bot.py", "w") as f:
    f.write(code)

