import psycopg2

uri = "postgresql://ponyadmin:AVNS_VWlShMNVWmd0Fcd8bk8@ai-pony-db-danislon-zombovich.d.aivencloud.com:20470/ponyadmin?sslmode=require"
try:
    conn = psycopg2.connect(uri)
    conn.autocommit = True
    cur = conn.cursor()
    
    cur.execute("CREATE SCHEMA IF NOT EXISTS ponyadmin;")
    cur.execute("SET search_path TO ponyadmin;")
    cur.execute("CREATE TABLE test_table (id serial PRIMARY KEY, data text);")
    print("Created table in ponyadmin schema!")
except Exception as e:
    print("Error:", e)
