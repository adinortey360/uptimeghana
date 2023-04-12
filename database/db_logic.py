import requests
import sqlite3

db_file = "sites.db"
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn

def create_entry(conn, entry):
    sql = '''INSERT INTO sites(name, company, url, category, popularity, image, downtime)
             VALUES(?, ?, ?, ?, ?, ?, ?)'''
    cursor = conn.cursor()
    cursor.execute(sql, entry)
    conn.commit()
    conn.close()
    


def update_entry(conn, entry):
    sql = '''UPDATE sites 
             SET name=?, 
                 company=?, 
                 url=?, 
                 category=?,
                 popularity=?,
                 image=?,
                 downtime=?,
             WHERE id=?'''
    cursor = conn.cursor()
    cursor.execute(sql, entry['id'])
    conn.commit()
    conn.close()