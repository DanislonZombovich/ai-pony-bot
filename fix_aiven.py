import requests

token = "m5hSRisS5KSlq0PP7N+n3l3dNrNAHrOBkg6VDerHIEhsJ4Dizx5PDyBtNGk5dkIf19V5Q8NCGUtWvoDeTLtk4KyilSj+O+7h9trkdlQZsVLgmER/7+SijVP3jJ5FFZ07Vlu8qHJrqyfgSYT1WoPJ8wCBOmo3q8Sns9du01v/C4L8IpCoefEHS6NSaKfs3EZJ4l67/eZx0hYjwdZujXixC54ilJFVCqed2UgmdxuotRygmY2t3bsU06TTu1AvgpBTbuMUO+EiUShPi2fn3PFtDMoe+l8IXIaw7uHmwj8nihDWxDo0wkjNwbh/8Ox0uchpEU0+O+VoedQ0T08UeKHJhPsYlIy28C0daajEsEsavCe+FFv+jcM3XUk="
project = "danislon-zombovich"
service = "discord-bot-pg"
headers = {"Authorization": f"aivenv1 {token}", "Content-Type": "application/json"}

# Reset the avnadmin password.
reset_url = f"https://api.aiven.io/v1/project/{project}/service/{service}/user/avnadmin/credentials/reset"
res = requests.post(reset_url, headers=headers)
print("Reset avnadmin password status:", res.status_code)

import time
time.sleep(5)

# Aiven's /v1/project/{project}/service/{service} actually returns the password inside service_uri_params.password
# Let's get it.
url = f"https://api.aiven.io/v1/project/{project}/service/{service}"
res2 = requests.get(url, headers=headers)
if res2.status_code == 200:
    srv = res2.json()["service"]
    params = srv.get("service_uri_params", {})
    user = params.get("user")
    password = params.get("password")
    host = params.get("host")
    port = params.get("port")
    dbname = params.get("dbname")
    
    uri = f"postgresql://{user}:{password}@{host}:{port}/{dbname}?sslmode=require"
    print("New Admin URI generated")
    
    with open("pg_uri.txt", "w") as f:
        f.write(uri)
else:
    print(res2.text)
