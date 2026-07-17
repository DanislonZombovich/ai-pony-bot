import requests
import json

token = "m5hSRisS5KSlq0PP7N+n3l3dNrNAHrOBkg6VDerHIEhsJ4Dizx5PDyBtNGk5dkIf19V5Q8NCGUtWvoDeTLtk4KyilSj+O+7h9trkdlQZsVLgmER/7+SijVP3jJ5FFZ07Vlu8qHJrqyfgSYT1WoPJ8wCBOmo3q8Sns9du01v/C4L8IpCoefEHS6NSaKfs3EZJ4l67/eZx0hYjwdZujXixC54ilJFVCqed2UgmdxuotRygmY2t3bsU06TTu1AvgpBTbuMUO+EiUShPi2fn3PFtDMoe+l8IXIaw7uHmwj8nihDWxDo0wkjNwbh/8Ox0uchpEU0+O+VoedQ0T08UeKHJhPsYlIy28C0daajEsEsavCe+FFv+jcM3XUk="
headers = {"Authorization": f"aivenv1 {token}", "Content-Type": "application/json"}

# List projects
res = requests.get(f"https://api.aiven.io/v1/project", headers=headers)
if res.status_code == 200:
    for p in res.json().get('projects', []):
        print("Project:", p['project_name'])
        res_s = requests.get(f"https://api.aiven.io/v1/project/{p['project_name']}/service", headers=headers)
        if res_s.status_code == 200:
            for s in res_s.json().get('services', []):
                print("  Service:", s['name'], s['plan'])
                print("  URI:", s['service_uri'])
                print("  Params:", s.get("service_uri_params"))
