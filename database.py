import json
import psycopg2

# Connect to PostgreSQL
connection = psycopg2.connect(
    host="localhost",
    database="samsung_phone_db",
    user="postgres",
    password="1233"
)

cursor = connection.cursor()

# Create table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS phones (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        url TEXT,
        specifications JSONB
    )
""")

# Read JSON file
with open("samsung_phones.json", "r", encoding="utf-8") as file:
    phones = json.load(file)

# Insert phone data
for phone in phones:
    cursor.execute(
        """
        INSERT INTO phones (name, url, specifications)
        VALUES (%s, %s, %s)
        """,
        (
            phone["name"],
            phone["url"],
            json.dumps(phone["specifications"])
        )
    )

connection.commit()

print(f"{len(phones)} phones inserted successfully!")

cursor.close()
connection.close()