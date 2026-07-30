import requests

GITHUB_TOKEN = "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"
headers = {"Authorization": f"token {GITHUB_TOKEN}"}
res = requests.get("https://api.github.com/user/repos", headers=headers)
for r in res.json():
    print(r["full_name"])
