from flask import Flask, render_template, request
from db_connector import DBConnector

app = Flask(__name__)
db_connector = DBConnector()

@app.route('/')
def index():
    # Fetch data from the database
    fetched_results = db_connector.get_all_draw_results()

    # Get the selected day from the request parameters
    selected_day = request.args.get('day')

    # Filter the data based on the selected day
    draw_results = []
    if selected_day == 'Wednesday':
        draw_results = [result for result in fetched_results if 'Wed' in result.draw_date]
    elif selected_day == 'Monday':
        draw_results = [result for result in fetched_results if 'Mon' in result.draw_date]
    else:
        draw_results = fetched_results    

    # Perform necessary data processing for visualization
    winning_numbers = []
    for draw_result in draw_results:
        winning_numbers.extend(draw_result.primary_numbers + draw_result.secondary_numbers)

    number_counts = {}
    for number in winning_numbers:
        number_counts[number] = number_counts.get(number, 0) + 1

    # Sort numbers by frequency in descending order
    sorted_numbers = sorted(number_counts.items(), key=lambda x: x[1], reverse=True)
    print(len(draw_results))
    print(len(sorted_numbers))
    # Pass the processed data to the HTML template
    return render_template('index-by-day.html', numbers=sorted_numbers, selected_day=selected_day)

if __name__ == '__main__':
    app.run()
