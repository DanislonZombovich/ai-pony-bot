import requests
import time

ptero_token = "ptlc_EP9hRjb7DE7HrSkyUlkyd8Yjz9zKUpa23MELHkjcOOk"
ptero_url = "https://control.heavencloud.in"
server_id = "822fe758" 

headers = {
    "Authorization": f"Bearer {ptero_token}",
    "Accept": "application/json",
    "Content-Type": "text/plain"
}

with open("bot.py", "rb") as f:
    requests.post(f"{ptero_url}/api/client/servers/{server_id}/files/write?file=bot.py", headers=headers, data=f.read())

h_json = {
    "Authorization": f"Bearer {ptero_token}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}
power_url = f"{ptero_url}/api/client/servers/{server_id}/power"
requests.post(power_url, headers=h_json, json={"signal": "kill"})
time.sleep(2)
requests.post(power_url, headers=h_json, json={"signal": "start"})
print("Server starting...")
