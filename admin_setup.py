import sqlite3

conn = sqlite3.connect('database.db')

conn.execute('''
CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
''')

conn.execute('''
INSERT OR IGNORE INTO admin (username, password)
VALUES ('admin', 'admin123')
''')

conn.commit()
conn.close()

print("Admin table created")
