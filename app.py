
from flask import Flask, jsonify, render_template
import sqlite3
from datetime import datetime
from lott import Lott
from db_connector import DBConnector

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lott-types')
def lott_types():
    return jsonify([lott.value for lott in Lott])

@app.route('/results/<lott_type>')
def get_results(lott_type):
    lott_enum = Lott(lott_type)
    db_connector = DBConnector()
    results = db_connector.get_all_draw_results(lott_enum)
    results_dict = [result.to_dict() for result in results]
    return jsonify(results_dict)

@app.route('/days')
def get_days():
    # Fetching all the draw_dates to extract unique days
    conn = sqlite3.connect('draw_results.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT draw_date FROM TUE UNION SELECT DISTINCT draw_date FROM MON_WED UNION SELECT DISTINCT draw_date FROM THU UNION SELECT DISTINCT draw_date FROM SAT UNION SELECT DISTINCT draw_date FROM SET4LIFE")
    dates = cursor.fetchall()
    
    # Extracting day names from dates
    days = set()
    for date_tuple in dates:
        date_str = date_tuple[0]
        date_obj = datetime.strptime(date_str, "%a, %d %b %Y")
        days.add(date_obj.strftime("%a"))
    
    return jsonify(list(days))

if __name__ == '__main__':
    app.run(debug=True)

