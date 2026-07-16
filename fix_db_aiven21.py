import psycopg2

uri = "postgresql://ponyuwfc:AVNS_yB_edBGf2uF-2ZYXOeT@discord-bot-pg-danislonzombovich.h.aivencloud.com:20470/ponyuwfc?sslmode=require"

try:
    conn = psycopg2.connect(uri)
    conn.autocommit = True
    cur = conn.cursor()
    
    # Check if we can create a schema since we are the db owner
    cur.execute("CREATE SCHEMA IF NOT EXISTS ponyuwfc;")
    cur.execute("SET search_path TO ponyuwfc;")
    cur.execute("CREATE TABLE IF NOT EXISTS test_table (id serial PRIMARY KEY, data text);")
    print("SUCCESS with ponyuwfc on ponyuwfc!")
except Exception as e:
    print("Error:", e)

