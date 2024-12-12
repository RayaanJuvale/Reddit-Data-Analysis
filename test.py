import pg8000

conn = pg8000.connect(
    host="localhost",  # or "db" if using Docker
    port=5432,
    database="reddit_data",
    user="postgres",
    password="Rayu45678&"
)
print("Connection successful!")
conn.close()
