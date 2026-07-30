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

run("apt-get update")
run("apt-get install -y docker.io git")

ssh.close()
