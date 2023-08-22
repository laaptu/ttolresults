from collections import defaultdict
from datetime import datetime
from db_connector import DBConnector
from lott import Lott
from flask import jsonify,json
from collections import OrderedDict

def fetch_lott_results(lott_type):
    lott = Lott(lott_type)
    results = fetch_lot_results_from_db(lott)
    
    all_primary_numbers = []
    all_secondary_numbers = []
    daywise_data = defaultdict(lambda: {"primary": [], "secondary": []})

    for draw_result in results:
        day = datetime.strptime(draw_result.draw_date, "%a, %d %b %Y").strftime('%A')
        all_primary_numbers.extend(draw_result.primary_numbers)
        all_secondary_numbers.extend(draw_result.secondary_numbers)
        daywise_data[day]["primary"].extend(draw_result.primary_numbers)
        daywise_data[day]["secondary"].extend(draw_result.secondary_numbers)

    occurrences = []

    for day, data in daywise_data.items():
        occurrences.append(append_data(day, data["primary"], data["secondary"]))


    # Add "All" entry
    all_data = append_data("All", all_primary_numbers,all_secondary_numbers)
    occurrences.append(all_data)

    return jsonify({
        "error": None,
        "response": {
            "Lott": lott.value,
            "days": list(daywise_data.keys()) + ["All"],
            "occurrences": occurrences
        }
    })

def append_data(day, primary_data, secondary_data):
    """
    Given a day, primary data, and secondary data, this function returns a dictionary
    containing the structured data for occurrences.
    """
    return {
        "day": day,
        "primaryNumOcc": getNumberOccurrences(primary_data),
        "secondaryNumOcc": getNumberOccurrences(secondary_data),
        "combinedNumOcc": getNumberOccurrences(primary_data + secondary_data)
    }


def getNumberOccurrences(numbers):
    """
    Given a list of numbers, this function returns a dictionary where the keys are
    the numbers and the values are the count of occurrences of each number.
    """
    occurrences = OrderedDict()
    
    for number in numbers:
        occurrences[number] = occurrences.get(number, 0) + 1

    # Sorting the dictionary based on the occurrences in descending order
    sorted_occurrences = OrderedDict(sorted(occurrences.items(), key=lambda item: item[1], reverse=True))
    # Convert the keys to strings
    return [f"{k}:{v}" for k, v in sorted_occurrences.items()]


def fetch_lot_results_from_db(lott):
    return DBConnector().get_all_draw_results(lott)

    
