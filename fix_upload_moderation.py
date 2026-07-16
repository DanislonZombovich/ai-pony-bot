import requests

ptero_token = "ptlc_EP9hRjb7DE7HrSkyUlkyd8Yjz9zKUpa23MELHkjcOOk"
ptero_url = "https://control.heavencloud.in"
server_id = "822fe758" 

headers = {
    "Authorization": f"Bearer {ptero_token}",
    "Accept": "application/json",
    "Content-Type": "text/plain"
}

with open("moderation.py", "rb") as f:
    content = f.read()

file_url = f"{ptero_url}/api/client/servers/{server_id}/files/write?file=moderation.py"
res = requests.post(file_url, headers=headers, data=content)
print("Uploaded moderation.py:", res.status_code)

h_json = {
    "Authorization": f"Bearer {ptero_token}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

power_url = f"{ptero_url}/api/client/servers/{server_id}/power"
requests.post(power_url, headers=h_json, json={"signal": "kill"})

import time
time.sleep(2)
requests.post(power_url, headers=h_json, json={"signal": "start"})
print("Server starting...")
