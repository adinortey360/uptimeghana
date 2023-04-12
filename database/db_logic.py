import datetime
import requests
import sqlite3


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn

def create_entry(conn, entry):
    sql = '''INSERT INTO sites(name, company, url, category, popularity, image, status_code, downtime)
             VALUES(?, ?, ?, ?, ?, ?, ?, ?)'''
    cursor = conn.cursor()
    cursor.execute(sql, entry)
    conn.commit()
    return cursor.lastrowid


def update_entry(conn, column_name, new_value, row_id):
    sql = f'''UPDATE sites 
              SET {column_name} = ?
              WHERE id = ?'''
    cursor = conn.cursor()
    cursor.execute(sql, (new_value, row_id))
    conn.commit()
    conn.close()

def fetch_all_entries(conn):
    '''Fetch all entries from the database.'''
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sites')
    rows = cursor.fetchall()
    return rows

def check_website_status(url, downtime):
    try:
        conn = create_connection('sites.db')
        response = requests.get(url)
        status_code = response.status_code
        if response.status_code == 200:
            # site is online
            cursor = conn.cursor()
            cursor.execute(f'UPDATE sites SET status_code = {response.status_code}, downtime = NULL WHERE url = ?', (url))
            conn.commit()
            conn.close()
            return 'Online', None
        else:
            # site is offline
            downtime = datetime.datetime.now()
            cursor = conn.cursor() 
            lastime_check = cursor.execute(f'SELECT downtime FROM sites WHERE url = ?', (url))
            time_difference = downtime - lastime_check
            cursor.execute('UPDATE sites SET downtime = ? WHERE url = ?', (downtime, url))
            conn.commit()
            conn.close()
            return 'Offline', time_difference
           
    except:
        Exception('Failed to fetch website status')
        return 'Error', downtime
    

sites = [
    ('mtngh', 'MTN', 'https://mtn.com.gh', 'telecom', 200, 'https://th.bing.com/th/id/OIP.QHy_DhuiJKv14Hv7T_cm7gHaGx?pid=ImgDet&rs=1', 403, False),
    ('vodafonegh', 'Vodafone', 'https://vodafone.com.gh', 'telecom', 5000, 'https://logos-world.net/wp-content/uploads/2020/09/Vodafone-Logo.png', 503, False),
    ('glogh', 'Glo', 'https://gloworld.com/gh', 'telecom', 234, 'https://www.gloworld.com/logo.png', 404, False),
    ('airteltigo', 'AirtelTigo', 'https://airteltigo.com.gh', 'telecom', 321,'https://airteltigo.com.gh/assets/img/logo.png', 404, False),
    ('ghanagov', 'Ghana.GOV', 'https://ghana.gov.gh', 'gov', 345, 'https://www.ghana.gov.gh/static/images/logos/gov-logo.png', 404, False),
    ('ghanaweb', 'GhanaWeb', 'https://ghanaweb.com', 'news', 242, 'https://cdn.ghanaweb.com/design/logo_desktop.png', 200, True),
    ('citifmonline', 'CitiFM', 'https://citinewsroom.com', 'news', 2, 'https://citinewsroom.com/wp-content/uploads/2019/08/cnr_logo_web.png', 404, False),
    ('graphic', 'Graphic', 'https://graphic.com.gh', 'news', 263, 'https://techera-gh.org/wp-content/uploads/2020/12/Daily-Graphic.jpg', 404, False),
    ('gra', 'GRA', 'https://gra.gov.gh', 'gov',  58, 'https://siga.gov.gh/wp-content/uploads/2020/09/Ghana-Revenue-Authority-GRA-Jobs-in-Ghana.jpg', 404, False),
    ('ghanahealthservice', 'Ghana Health Service', 'https://ghs.gov.gh', 'gov', 3, 'https://ghs.gov.gh/wp-content/uploads/2022/06/logo.png', 404, False),
    ('moh', 'MoH', 'https://moh.gov.gh', 'gov', 6, 'https://www.moh.gov.gh/wp-content/uploads/2019/07/moh-xl.png', 404, False),
]

# db_file = 'sites.db'
# for site in sites:
#     conn = create_connection(db_file)
#     if conn:
#         entry = (site[0], site[1], site[2], site[3], site[4], site[5], site[6], site[7])
#         entry_id = create_entry(conn, entry)
#         print(f'Entry created with ID: {entry_id}')
#     else:
#         print(f'Error! Cannot establish connection to database')

    