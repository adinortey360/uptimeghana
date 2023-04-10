from flask import Flask, render_template
import requests
import sqlite3
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    conn = sqlite3.connect('sites.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, url, downtime FROM sites')
    sites = cursor.fetchall()
    conn.close()

    status_dict = {}
    for site in sites:
        name = site[0]
        url = site[1]
        downtime = site[2]
        status, downtime = check_website_status(url, downtime)
        status_dict[name] = {'status': status, 'downtime': downtime}

    return render_template('index.html', status_dict=status_dict)

def check_website_status(url, downtime):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            if downtime is not None:
                # site is back online
                conn = sqlite3.connect('sites.db')
                cursor = conn.cursor()
                cursor.execute('UPDATE sites SET downtime=NULL WHERE url=?', (url,))
                conn.commit()
                conn.close()

            return 'Online', None
        else:
            if downtime is None:
                # site just went down
                downtime = datetime.datetime.now()
                conn = sqlite3.connect('sites.db')
                cursor = conn.cursor()
                cursor.execute('UPDATE sites SET downtime=? WHERE url=?', (downtime, url))
                conn.commit()
                conn.close()

            return 'Offline', downtime
    except:
        if downtime is None:
            # site just went down
            downtime = datetime.datetime.now()
            conn = sqlite3.connect('sites.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE sites SET downtime=? WHERE url=?', (downtime, url))
            conn.commit()
            conn.close()

        return 'Error', downtime

if __name__ == '__main__':
    app.run(debug=True)
