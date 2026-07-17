import requests

ptero_token = "ptlc_EP9hRjb7DE7HrSkyUlkyd8Yjz9zKUpa23MELHkjcOOk"
ptero_url = "https://control.heavencloud.in"
server_id = "822fe758" 

h_json = {
    "Authorization": f"Bearer {ptero_token}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

power_url = f"{ptero_url}/api/client/servers/{server_id}/power"
requests.post(power_url, headers=h_json, json={"signal": "start"})
print("Sent start signal.")
