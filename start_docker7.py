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
        pass
    for line in iter(stderr.readline, ""):
        pass

run("docker logs --tail 20 ai-pony-bot-container")
ssh.close()
