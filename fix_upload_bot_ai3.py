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

files_to_upload = ["ai_core.py", "live_voice.py"]

for f_name in files_to_upload:
    with open(f_name, "rb") as f:
        res = requests.post(f"{ptero_url}/api/client/servers/{server_id}/files/write?file={f_name}", headers=headers, data=f.read())
        print(f"Uploaded {f_name}:", res.status_code)

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
