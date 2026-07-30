import paramiko
import time

host = "213.176.116.243"
user = "root"
pwd = "L02z14sDNbsC"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username=user, password=pwd)

stdin, stdout, stderr = ssh.exec_command("docker logs --tail 200 ai-pony-bot-container | grep -i voice")
print(stdout.read().decode())
ssh.close()
