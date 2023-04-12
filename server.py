from flask import Flask, render_template
import requests
import sqlite3
import datetime
from database import db_logic

app = Flask(__name__)

@app.route('/')
def index():
    # conn = sqlite3.connect('sites.db')
    # cursor = conn.cursor()
    # cursor.execute('SELECT name, url, downtime FROM sites')
    # sites = cursor.fetchall()
    # conn.close()

    conn = db_logic.create_connection('./database/sites.db')
    sites = db_logic.fetch_all_entries(conn)
    status_dict = {}
    for site in sites:
        name = site[1]
        company = site[2]
        url = site[3]
        category = site[4]
        popularity = site[5]
        image = site[6]
        status_code = site[7]
        downtime = site[8]
        # status, downtime = check_website_status(url, downtime)
        status_dict[name] = {
            'company': company,
            'url': url,
            'category': category,
            'popularity': popularity,
            'logo': image,
            'status_code': status_code,
            'downtime': downtime,
        }

    return render_template('index.html', status_dict=status_dict)



def check_website_status(url):
    try:
        conn = db_logic.create_connection('./database/sites.db')
        downtime = datetime.datetime.now()
        response = requests.get(url)
        if response.status_code == 200:
            cursor = conn.cursor()
            cursor.execute('UPDATE sites SET downtime = ? WHERE url = ?', (downtime, url))
            conn.commit()
            conn.close()
            return 'Online', None
        else:
            cursor = conn.cursor()
            last_check = cursor.execute('SELECT downtime FROM sites WHERE url = ?', (url,))
            uptime_diff = downtime - last_check
            cursor = conn.cursor()
            cursor.execute('UPDATE sites SET downtime = ? WHERE url = ?',(uptime_diff, url))
            conn.commit()
            conn.close()
            return 'Offline', uptime_diff
    except:
        Exception('Failed to check website status')
        return 'Error', downtime

if __name__ == '__main__':
    app.run(debug=True)