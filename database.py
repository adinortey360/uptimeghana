import sqlite3

conn = sqlite3.connect('sites.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE sites (
    id INTEGER PRIMARY KEY,
    name TEXT,
    url TEXT,
    downtime DATETIME DEFAULT NULL
)
''')

conn.commit()
conn.close()
