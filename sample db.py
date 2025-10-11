import sqlite3

conn = sqlite3.connect("fin.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    type TEXT,
    amount REAL,
    note TEXT,
    date TEXT
)
""")

# Optional: insert example user
c.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ("testuser", "12345"))

conn.commit()
conn.close()

print("Database created successfully!")
