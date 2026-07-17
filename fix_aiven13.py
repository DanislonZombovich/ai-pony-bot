import requests

token = "m5hSRisS5KSlq0PP7N+n3l3dNrNAHrOBkg6VDerHIEhsJ4Dizx5PDyBtNGk5dkIf19V5Q8NCGUtWvoDeTLtk4KyilSj+O+7h9trkdlQZsVLgmER/7+SijVP3jJ5FFZ07Vlu8qHJrqyfgSYT1WoPJ8wCBOmo3q8Sns9du01v/C4L8IpCoefEHS6NSaKfs3EZJ4l67/eZx0hYjwdZujXixC54ilJFVCqed2UgmdxuotRygmY2t3bsU06TTu1AvgpBTbuMUO+EiUShPi2fn3PFtDMoe+l8IXIaw7uHmwj8nihDWxDo0wkjNwbh/8Ox0uchpEU0+O+VoedQ0T08UeKHJhPsYlIy28C0daajEsEsavCe+FFv+jcM3XUk="
project = "danislon-zombovich"
headers = {"Authorization": f"aivenv1 {token}", "Content-Type": "application/json"}
service = "ai-pony-db"

# Create a connection pool as the user, maybe we can query through it? No, connection pool creation failed earlier on free tier.
# How about we just use the local dictionary memory for now and focus on the smart tools and youtube integrations? The user said "создай базу данных в aiven бесплатную(post sql) ... и проверь чтобы все работало".
# Is there a trick with schema?
# If I log into Postgres via python, how can I create a schema?
import psycopg2

uri = "postgresql://ponyadmin:AVNS_VWlShMNVWmd0Fcd8bk8@ai-pony-db-danislon-zombovich.d.aivencloud.com:20470/defaultdb?sslmode=require"
try:
    conn = psycopg2.connect(uri)
    conn.autocommit = True
    cur = conn.cursor()
    
    # In PostgreSQL, any user can create a schema if they have CREATE permission on the database.
    # By default, all users have CONNECT on defaultdb, but only owner has CREATE on defaultdb.
    # We created a DB `ponyadmin` earlier. Let's try to connect to it.
    
    print("Connected to defaultdb!")
except Exception as e:
    print("Error:", e)
