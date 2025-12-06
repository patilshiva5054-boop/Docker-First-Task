import psycopg2
import time

# Wait for Postgres to be ready
time.sleep(3)

try:
    conn = psycopg2.connect(
        host="my-postgres",
        database="mydb",
        user="postgres",
        password="postgres"
    )
    print("Connected to DB successfully!")
    conn.close()
except Exception as e:
    print("Error:", e)
