import os
import time
import psycopg2

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "db")   # service name used by docker-compose
POSTGRES_DB = os.getenv("POSTGRES_DB", "mydb")
POSTGRES_USER = os.getenv("POSTGRES_USER", "user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "pass")
RETRY_COUNT = 30
SLEEP_SECONDS = 2

def wait_for_postgres():
    for i in range(RETRY_COUNT):
        try:
            conn = psycopg2.connect(
                host=POSTGRES_HOST,
                database=POSTGRES_DB,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
                connect_timeout=3
            )
            conn.close()
            print("Postgres is reachable.")
            return True
        except Exception as e:
            print(f"Waiting for Postgres... ({i+1}/{RETRY_COUNT}) -> {e}")
            time.sleep(SLEEP_SECONDS)
    return False

def main():
    ok = wait_for_postgres()
    if not ok:
        print("Postgres did not become ready - exiting.")
        return

    conn = psycopg2.connect(
        host=POSTGRES_HOST,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            text TEXT NOT NULL
        );
    """)
    conn.commit()

    cur.execute("INSERT INTO messages (text) VALUES (%s) RETURNING id;", ("Hello from Dockerized Python!",))
    inserted_id = cur.fetchone()[0]
    conn.commit()

    cur.execute("SELECT id, text FROM messages WHERE id = %s;", (inserted_id,))
    row = cur.fetchone()
    print("Inserted row:", row)

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
