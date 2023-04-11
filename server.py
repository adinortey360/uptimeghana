from flask import Flask, render_template
import requests
import sqlite3
import datetime

app = Flask(__name__)

# TODO: Use database instead of list
sites = [
    ('mtngh', 'MTN', 'https://mtn.com.gh', 'telecom', 200, False),
    ('vodafonegh', 'Vodafone', 'https://vodafone.com.gh', 'telecom', 5000, False),
    ('airtelgh', 'Airtel', 'https://airtel.com.gh', 'telecom', 855, True),
    ('glogh', 'Glo', 'https://glo.com.gh', 'telecom', 234, False),
    ('airteltigo', 'AirtelTigo', 'https://airteltigo.com', 321, 'telecom', False),
    ('ghanagov', 'Ghana.GOV', 'https://ghana.gov.gh', 'gov', 345, False),
    ('ghanaweb', 'GhanaWeb', 'https://ghanaweb.com', 'news', 242, True),
    ('citifmonline', 'CitiFM', 'https://citifmonline.com', 'news', 2, False),
    ('graphic', 'Graphic', 'https://graphic.com.gh', 'news', 263, False),
    ('gra', 'GRA', 'https://gra.gov.gh', 'gov',  58, False),
    ('ghanahealthservice', 'Ghana Health Service', 'https://ghanahealthservice.org', 'gov', 3, False),
]



@app.route('/')
def index():
    # conn = sqlite3.connect('sites.db')
    # cursor = conn.cursor()
    # cursor.execute('SELECT name, url, downtime FROM sites')
    # sites = cursor.fetchall()
    # conn.close()

    

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
