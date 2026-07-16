import requests

token = "m5hSRisS5KSlq0PP7N+n3l3dNrNAHrOBkg6VDerHIEhsJ4Dizx5PDyBtNGk5dkIf19V5Q8NCGUtWvoDeTLtk4KyilSj+O+7h9trkdlQZsVLgmER/7+SijVP3jJ5FFZ07Vlu8qHJrqyfgSYT1WoPJ8wCBOmo3q8Sns9du01v/C4L8IpCoefEHS6NSaKfs3EZJ4l67/eZx0hYjwdZujXixC54ilJFVCqed2UgmdxuotRygmY2t3bsU06TTu1AvgpBTbuMUO+EiUShPi2fn3PFtDMoe+l8IXIaw7uHmwj8nihDWxDo0wkjNwbh/8Ox0uchpEU0+O+VoedQ0T08UeKHJhPsYlIy28C0daajEsEsavCe+FFv+jcM3XUk="
project = "danislon-zombovich"
service = "discord-bot-pg"
headers = {"Authorization": f"aivenv1 {token}", "Content-Type": "application/json"}

# Can we get the password for avnadmin by getting the specific user?
url = f"https://api.aiven.io/v1/project/{project}/service/{service}/user/avnadmin"
res = requests.get(url, headers=headers)
if res.status_code == 200:
    print(res.json())
else:
    print(res.status_code, res.text)
