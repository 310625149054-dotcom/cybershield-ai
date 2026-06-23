import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

try:
    cursor.execute("""
    ALTER TABLE scans
    ADD COLUMN explanation TEXT
    """)
    print("Database fixed successfully")
except Exception as e:
    print("Error:", e)

conn.commit()
conn.close()