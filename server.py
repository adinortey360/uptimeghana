from flask import Flask, render_template
from database import db_logic

app = Flask(__name__)

@app.route('/')
def index():
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
        db_logic.check_website_status(url, downtime)

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

if __name__ == '__main__':
    app.run(debug=True)