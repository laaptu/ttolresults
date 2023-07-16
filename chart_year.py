from flask import Flask, render_template
from db_connector import DBConnector
from draw_result import DrawResult

app = Flask(__name__)

# Create a route to fetch all draw_results and generate filters
@app.route('/chart')
def drawResultChart():
    # Fetch all draw_results from the database
    db_connector = DBConnector()
    draw_results = db_connector.get_all_draw_results()

    # Extract unique years from draw_date and create a list of filters
    filters = sorted(list(set([draw_result.draw_date.split(', ')[-1].split()[-1] for draw_result in draw_results])), reverse=True)

    # Serialize the draw_results
    serialized_draw_results = [draw_result.to_dict() for draw_result in draw_results]

    return render_template('chart-year.html', draw_results=serialized_draw_results, filters=filters)


if __name__ == '__main__':
    app.run()
