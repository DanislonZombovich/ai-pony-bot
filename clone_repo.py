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
    exit_status = stdout.channel.recv_exit_status() 
    if exit_status == 0:
        print("Success")
    else:
        print("Error:", stderr.read().decode())

run("rm -rf /opt/ai-pony-bot")
run("git clone https://github.com/DanislonZombovich/ai-pony-bot.git /opt/ai-pony-bot")

# Create Dockerfile
dockerfile = """
FROM python:3.12-slim

RUN apt-get update && apt-get install -y \\
    ffmpeg \\
    libsodium-dev \\
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
"""

cmd_create_dockerfile = f"cat << 'INNER_EOF' > /opt/ai-pony-bot/Dockerfile\n{dockerfile}\nINNER_EOF"
run(cmd_create_dockerfile)

# Create .env
env_content = """
DISCORD_TOKEN="MTUyNzA4NDQ5MjYwNTM1ODE5NA.GZChvM.U1BMra4xBjXbnABUIg6e0Hbye_g-o-d-z9U2yg"
GEMINI_API_KEY="AQ.Ab8RN6IRu6jUvkT-r4O-YhFgCPIId0kvy9k6CFaWJzZAGqS82A"
AIVEN_URI=""
ADMIN_ID=862759084200558609
"""

cmd_create_env = f"cat << 'INNER_EOF' > /opt/ai-pony-bot/.env\n{env_content}\nINNER_EOF"
run(cmd_create_env)

ssh.close()
