import requests
import time

token = "m5hSRisS5KSlq0PP7N+n3l3dNrNAHrOBkg6VDerHIEhsJ4Dizx5PDyBtNGk5dkIf19V5Q8NCGUtWvoDeTLtk4KyilSj+O+7h9trkdlQZsVLgmER/7+SijVP3jJ5FFZ07Vlu8qHJrqyfgSYT1WoPJ8wCBOmo3q8Sns9du01v/C4L8IpCoefEHS6NSaKfs3EZJ4l67/eZx0hYjwdZujXixC54ilJFVCqed2UgmdxuotRygmY2t3bsU06TTu1AvgpBTbuMUO+EiUShPi2fn3PFtDMoe+l8IXIaw7uHmwj8nihDWxDo0wkjNwbh/8Ox0uchpEU0+O+VoedQ0T08UeKHJhPsYlIy28C0daajEsEsavCe+FFv+jcM3XUk="
project = "danislon-zombovich"
headers = {"Authorization": f"aivenv1 {token}", "Content-Type": "application/json"}
service = "ai-pony-db"

print("Waiting for service to be active...")
for _ in range(30):
    res = requests.get(f"https://api.aiven.io/v1/project/{project}/service/{service}", headers=headers)
    if res.status_code == 200:
        state = res.json()["service"]["state"]
        if state == "RUNNING":
            print("Service RUNNING.")
            break
        print(f"State: {state}...")
    time.sleep(5)

# Reset password to get it
res_pwd = requests.post(f"https://api.aiven.io/v1/project/{project}/service/{service}/user/avnadmin/credentials/reset", headers=headers)

time.sleep(2)
# Re-fetch service to see if URI has the new password in params or just use list users
res_u = requests.get(f"https://api.aiven.io/v1/project/{project}/service/{service}/user", headers=headers)
if res_u.status_code == 200:
    for u in res_u.json()["users"]:
        if u["username"] == "avnadmin":
            pwd = u["password"]
            uri = f"postgresql://avnadmin:{pwd}@ai-pony-db-danislon-zombovich.d.aivencloud.com:20470/defaultdb?sslmode=require"
            print("URI:", uri)
            with open("aiven_uri.txt", "w") as f:
                f.write(uri)
