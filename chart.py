from flask import Flask, render_template
from db_connector import DBConnector

app = Flask(__name__)
db_connector = DBConnector()

@app.route('/')
def index():
    # Fetch data from the database
    draw_results = db_connector.get_all_draw_results()

    # Perform necessary data processing for visualization
    winning_numbers = []
    for draw_result in draw_results:
        winning_numbers.extend(draw_result.primary_numbers + draw_result.secondary_numbers)

    number_counts = {}
    for number in winning_numbers:
        number_counts[number] = number_counts.get(number, 0) + 1

    # Sort numbers by frequency in descending order
    sorted_numbers = sorted(number_counts.items(), key=lambda x: x[1], reverse=True)

    # Pass the processed data to the HTML template
    return render_template('index.html', numbers=sorted_numbers)

if __name__ == '__main__':
    app.run()

    
