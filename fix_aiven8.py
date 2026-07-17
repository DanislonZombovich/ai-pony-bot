import requests

token = "m5hSRisS5KSlq0PP7N+n3l3dNrNAHrOBkg6VDerHIEhsJ4Dizx5PDyBtNGk5dkIf19V5Q8NCGUtWvoDeTLtk4KyilSj+O+7h9trkdlQZsVLgmER/7+SijVP3jJ5FFZ07Vlu8qHJrqyfgSYT1WoPJ8wCBOmo3q8Sns9du01v/C4L8IpCoefEHS6NSaKfs3EZJ4l67/eZx0hYjwdZujXixC54ilJFVCqed2UgmdxuotRygmY2t3bsU06TTu1AvgpBTbuMUO+EiUShPi2fn3PFtDMoe+l8IXIaw7uHmwj8nihDWxDo0wkjNwbh/8Ox0uchpEU0+O+VoedQ0T08UeKHJhPsYlIy28C0daajEsEsavCe+FFv+jcM3XUk="
project = "danislon-zombovich"
headers = {"Authorization": f"aivenv1 {token}", "Content-Type": "application/json"}
service = "ai-pony-db"

# Aiven returns the password in users list only when explicitly creating the user, not when resetting.
import random, string
new_user = "ponyadmin"

res_u = requests.post(f"https://api.aiven.io/v1/project/{project}/service/{service}/user", headers=headers, json={"username": new_user})
if res_u.status_code == 200:
    pwd = res_u.json()["user"]["password"]
    uri = f"postgresql://{new_user}:{pwd}@ai-pony-db-danislon-zombovich.d.aivencloud.com:20470/defaultdb?sslmode=require"
    print("New URI:", uri)
    with open("aiven_uri.txt", "w") as f:
        f.write(uri)
else:
    print(res_u.text)
