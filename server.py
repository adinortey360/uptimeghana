from flask import Flask, render_template
import requests
import sqlite3
import datetime

app = Flask(__name__)

# TODO: Use database instead of list
sites = [
    ('mtngh', 'MTN', 'mtn.com.gh', 'telecom', 200, False),
    ('vodafonegh', 'Vodafone', 'vodafone.com.gh', 'telecom', 5000, False),
    ('airtelgh', 'Airtel', 'airtel.com.gh', 'telecom', 855, True),
    ('glogh', 'Glo', 'glo.com.gh', 'telecom', 234, False),
    ('airteltigo', 'AirtelTigo', 'airteltigo.com', 321, 'telecom', False),
    ('ghanagov', 'Ghana.GOV', 'ghana.gov.gh', 'gov', 345, False),
    ('ghanaweb', 'GhanaWeb', 'ghanaweb.com', 'news', 242, True),
    ('citifmonline', 'CitiFM', 'citifmonline.com', 'news', 2, False),
    ('graphic', 'Graphic', 'graphic.com.gh', 'news', 263, False),
    ('gra', 'GRA', 'gra.gov.gh', 'gov',  58, False),
    ('ghanahealthservice', 'Ghana Health Service', 'ghanahealthservice.org', 'gov', 3, False),
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
        company = site[1]
        url = site[2]
        category = site[3]
        popularity = site[4]
        downtime = site[5]
        # status, downtime = check_website_status(url, downtime)
        status_dict[name] = {
            'company': company,
            'url': url,
            'category': category,
            'popularity': popularity,
            'downtime': downtime,
        }

    return render_template('index.html', status_dict=status_dict)



# Update the database with website entries
def create_entry(conn, entry):
    """Update an entry in the database."""
    sql = '''UPDATE sites 
             SET name = ?,
                 url = ?,
                 image = ?'''

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
