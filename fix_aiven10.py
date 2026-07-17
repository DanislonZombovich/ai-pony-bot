import requests

token = "m5hSRisS5KSlq0PP7N+n3l3dNrNAHrOBkg6VDerHIEhsJ4Dizx5PDyBtNGk5dkIf19V5Q8NCGUtWvoDeTLtk4KyilSj+O+7h9trkdlQZsVLgmER/7+SijVP3jJ5FFZ07Vlu8qHJrqyfgSYT1WoPJ8wCBOmo3q8Sns9du01v/C4L8IpCoefEHS6NSaKfs3EZJ4l67/eZx0hYjwdZujXixC54ilJFVCqed2UgmdxuotRygmY2t3bsU06TTu1AvgpBTbuMUO+EiUShPi2fn3PFtDMoe+l8IXIaw7uHmwj8nihDWxDo0wkjNwbh/8Ox0uchpEU0+O+VoedQ0T08UeKHJhPsYlIy28C0daajEsEsavCe+FFv+jcM3XUk="
project = "danislon-zombovich"
headers = {"Authorization": f"aivenv1 {token}", "Content-Type": "application/json"}
service = "ai-pony-db"

# Actually Aiven connection pool returns password maybe? No.
# Instead of Aiven for PostgreSQL, is it possible we just fetch the Service URI endpoint properly to get avnadmin password?
url = f"https://api.aiven.io/v1/project/{project}/service/{service}"
res = requests.get(url, headers=headers)
print(res.json()["service"]["service_uri"]) # Will have <redacted>

