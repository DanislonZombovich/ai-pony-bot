import paramiko
import time

host = "213.176.116.243"
user = "root"
pwd = "L02z14sDNbsC"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username=user, password=pwd)

time.sleep(5)
stdin, stdout, stderr = ssh.exec_command("docker logs --tail 20 ai-pony-bot-container")
print(stdout.read().decode())
print(stderr.read().decode())
ssh.close()
