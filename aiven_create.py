import requests

AIVEN_TOKEN = "5Iwrdjj99sktRCZeMR1P1mhOrZiGu5DsPLrk7li3QLxYXdqD2MaHLvc9Sat/tEgTzu1EIw/Ie0yjevIW2MyekEH0BqBai9zaA++Q3UZDnN3Dhog29+zAN1NJhqLj3kFsSo59wzMxdMG399iwnJC1+Xtu26W+MV1yoNWwYvNi1Od1PwQi3bi7cbw6hQJ/UkLbwNApJKUdnahdQ/fQ3zXuyZPj+Z7A19HK0XvUjeHpLzvv/Xwc3iCrQ3N6zHJVzQBFYS76/xa2QHZ6RoQg3AgqbPBWZDAVv21fLL/0lvKqLyAUJbRF/Jpy+Qamr0hmIN54crbGaGoOmSYYxP5UCgLq73QJl4sXu6dVKaOoekwZnf5unbig4xmPa5I="
PROJECT = "danislonzombovich"
SERVICE_NAME = "discord-bot-pg"

headers = {
    "Authorization": f"aivenv1 {AIVEN_TOKEN}"
}

svc_res = requests.get(f"https://api.aiven.io/v1/project/{PROJECT}/service/{SERVICE_NAME}", headers=headers)
svc_data = svc_res.json()
params = svc_data["service"]["service_uri_params"]
host = params["host"]
port = params["port"]
password = params["password"]
user = params["user"]

uri = f"postgresql://{user}:{password}@{host}:{port}/defaultdb?sslmode=require"
print(uri)
