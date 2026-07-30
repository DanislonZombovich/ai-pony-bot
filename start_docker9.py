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

# The build was still running in background, let's wait for it to finish and run it properly
run("cd /opt/ai-pony-bot && docker build -t ai-pony-bot .")
run("docker rm -f ai-pony-bot-container || true")
run("cd /opt/ai-pony-bot && docker run -d --name ai-pony-bot-container --restart unless-stopped -v /opt/ai-pony-bot/memory:/app/memory ai-pony-bot")

ssh.close()
