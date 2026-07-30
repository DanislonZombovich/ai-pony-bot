import subprocess

def run(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    print(err.decode(), out.decode())

run("git remote set-url origin https://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@github.com/DanislonZombovich/ai-pony-bot.git")
run("git push -u origin master:main -f")
