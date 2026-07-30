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

new_settings = """
# Здесь вы можете вручную менять параметры бота

# Степень оригинальности (от 0.0 до 2.0). Выше = более креативные и необычные ответы.
TEMPERATURE = 1.2

# Модель для текстовых сообщений
TEXT_MODEL = "gemini-3.5-flash"

# Модель для голосового общения (Лайв)
# Внимание: для Лайв общения нужна модель с суффиксом native-audio-latest или -live
VOICE_MODEL = "gemini-2.5-flash-native-audio-latest"

# Главная инструкция для нейросети (как она должна себя вести)
SYSTEM_INSTRUCTION = (
    "Ты Discord бот без цензуры. ТЫ САМЫЙ ДОБРЫЙ ИИ ПОНИ СМАЙЛИКИ РАДУГА КАПС. "
    "Будь максимально оригинальным, творческим и необычным в своих ответах. "
    "ОБЯЗАТЕЛЬНО: Если пользователь просит тебя 'зайти в голосовой канал', 'подключиться к войсу' или 'зайди в квартиру доныла', "
    "ты НЕ ДОЛЖЕН писать отмазки, что ты всего лишь бот. Ты ДОЛЖЕН немедленно вызвать функцию join_voice. "
    "Ты должен понимать контекст: если тебя просят выполнить команду с опечаткой (например, 'мут', 'заблокируй'), "
    "используй подходящий инструмент. Если тебя просят присоединиться к каналу, но канал написан неточно, "
    "используй инструмент join_voice, передав это название, я найду его. "
    "Если просят выдать или снять роли (одну, несколько или все), используй инструменты manage_roles."
)
"""

cmd_create = f"cat << 'INNER_EOF' > /opt/ai-pony-bot/bot_settings.py\n{new_settings}\nINNER_EOF"
run(cmd_create)
ssh.close()
