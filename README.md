# Docker-First-Task
 Docker for Absolute Beginners — Full Practical Guide (README)

This project teaches you Docker from scratch by building, running, networking, and Dockerizing a real Python + PostgreSQL application.

 1. Prerequisites
Install Docker Desktop

Download Docker Desktop from:
https://www.docker.com/products/docker-desktop

Install VS Code

https://code.visualstudio.com/

Recommended VS Code Extensions

Docker (by Microsoft)

Remote - Containers (optional but useful)

To verify Docker is connected to VS Code:

Open VS Code

Click Docker icon (left side)

You should see:

Containers

Images

Networks

Volumes

If you don’t see them → start Docker Desktop.

 2. Pulling Images from Docker Hub

Docker Hub:
https://hub.docker.com/

Example: pull Ubuntu image

docker pull ubuntu


List downloaded images:

docker images

 3. Create a Simple Python App

Create a new folder:

Docker-Project/


Create a file:

app.py
print("Hello from inside a Docker container!")

 4. Create a Dockerfile

Inside the same folder, create:

Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY app.py .

CMD ["python", "app.py"]

 5. Build and Run the Docker Image

Build the image:

docker build -t my-python-app .


Run the container:

docker run my-python-app


Expected output:

Hello from inside a Docker container!

 6. Clean Up Docker Resources

Stop a container:

docker stop <id>


Remove:

docker rm <id>


Remove image:

docker rmi my-python-app

 7. Create a Docker Network + PostgreSQL Container

Create a network:

docker network create mynetwork


Run PostgreSQL:

docker run -d \
  --name my-postgres \
  --network mynetwork \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=mydb \
  postgres


Check if running:

docker ps

8. Python App That Connects to PostgreSQL

Use psycopg2 to connect.

app.py (database version)
import psycopg2
import time

time.sleep(3)

try:
    conn = psycopg2.connect(
        host="my-postgres",
        database="mydb",
        user="postgres",
        password="postgres"
    )
    print("Connected to the database!")
    conn.close()
except Exception as e:
    print("Connection failed:", e)

Updated Dockerfile:
FROM python:3.10-slim

WORKDIR /app

COPY app.py .

RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*
RUN pip install psycopg2-binary

CMD ["python", "app.py"]


Rebuild image:

docker build -t my-python-db-app .


Run with the same network:

docker run --rm --network mynetwork my-python-db-app


Expected output:

Connected to the database!

 9. Beginner Mini-Project (Final Task)

You will now create a Python app that:

✔ Connects to PostgreSQL
✔ Creates a table
✔ Inserts one row
✔ Reads and prints all rows
✔ Runs fully inside Docker
✔ Connects via custom Docker network

 Final Project — Code
app.py
import psycopg2
import time

time.sleep(3)

try:
    conn = psycopg2.connect(
        host="my-postgres",
        database="mydb",
        user="postgres",
        password="postgres"
    )
    cursor = conn.cursor()

    print("\nConnected to DB successfully!\n")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100)
        );
    """)
    conn.commit()

    cursor.execute("INSERT INTO students (name) VALUES ('Shiva')")
    conn.commit()

    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()

    print("Rows in DB:")
    for row in rows:
        print(row)

    cursor.close()
    conn.close()

except Exception as e:
    print("Error:", e)

Final Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY app.py .

RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*
RUN pip install psycopg2-binary

CMD ["python", "app.py"]

🛠 Run the Full Project
Start PostgreSQL
docker run -d --name my-postgres --network mynetwork \
-e POSTGRES_USER=postgres \
-e POSTGRES_PASSWORD=postgres \
-e POSTGRES_DB=mydb \
postgres

Build app
docker build -t my-python-db-app .

Run app
docker run --rm --network mynetwork my-python-db-app

Expected Output
Connected to DB successfully!

Rows in DB:
(1, 'Shiva')

10. Push Image to Docker Hub

Log in:

docker login


Tag your image:

docker tag my-python-db-app your-dockerhub-username/my-python-db-app


Push it:

docker push your-dockerhub-username/my-python-db-app


Done! 🚀

✔ Project Completed

This guide taught you:

How to install and use Docker Desktop

How to work with Docker in VS Code

Build Docker images

Run containers

Create Docker networks

Run PostgreSQL in Docker

Connect Python → PostgreSQL

Dockerize a full app

Push image to Docker Hub