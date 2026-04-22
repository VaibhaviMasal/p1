import sqlite3

conn = sqlite3.connect('database.db')
conn.execute('''
CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT,
    faculty TEXT,
    rating INTEGER,
    comment TEXT
)
''')
conn.commit()
conn.close()

print("Database created successfully")
