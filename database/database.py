import sqlite3

conn = sqlite3.connect('sites.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE sites (
    id INTEGER PRIMARY KEY AUTO INCREMENT,
    name TEXT,
    company TEXT,
    url TEXT,
    category TEXT,
    popularity INTEGER,
    image TEXT,
    downtime DATETIME DEFAULT NULL
)
''')

conn.commit()
conn.close()
