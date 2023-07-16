import requests
from datetime import datetime
from calendar import monthrange

from db_connector import DBConnector
from draw_result import DrawResult
from frequency import Frequency


def get_draw_results(date, frequency=Frequency.MONTHLY):
    if frequency == Frequency.DAILY:
        date_start = date.replace(hour=14, minute=0, second=0, microsecond=0).isoformat() + 'Z'
        date_end = date.replace(hour=13, minute=59, second=59, microsecond=0).isoformat() + 'Z'
    else:
        _, last_day = monthrange(date.year, date.month)
        date_start = date.replace(day=1, hour=14, minute=0, second=0, microsecond=0).isoformat() + 'Z'
        date_end = date.replace(day=last_day, hour=13, minute=59, second=59, microsecond=0).isoformat() + 'Z'

    url = "https://data.api.thelott.com/sales/vmax/web/data/lotto/results/search/daterange"
    payload = {
        "DateStart": date_start,
        "DateEnd": date_end,
        "ProductFilter": ["MonWedLotto"],
        "CompanyFilter": ["Tattersalls"]
    }
    response = requests.post(url, json=payload)

    if response.ok:
        data = response.json()
        if data.get("Success"):
            draw_results = []

            for result in data.get("Draws", []):
                draw_number = result.get("DrawNumber")
                draw_date_str = result.get("DrawDate")
                primary_numbers = result.get("PrimaryNumbers")
                secondary_numbers = result.get("SecondaryNumbers")

                draw_date = datetime.strptime(draw_date_str, "%Y-%m-%dT%H:%M:%S")
                formatted_draw_date = draw_date.strftime("%a, %d %b %Y")

                draw_result = DrawResult(draw_number, formatted_draw_date, primary_numbers, secondary_numbers)
                draw_results.append(draw_result)

            return draw_results
        else:
            error_info = data.get("ErrorInfo")
            print(f"API error: {error_info}")
    else:
        print("API request failed.")

    return None

# Usage example
# date = datetime(2022, 7, 31)  # Example date
# frequency = Frequency.MONTHLY  # Example frequency

# draw_results = get_draw_results(date, frequency)

# if draw_results:
#     for drawResult in draw_results:
#         drawResult.print()
#     db_connector = DBConnector()
#     db_connector.save_draw_results(draw_results)
#     print("DrawResults saved successfully!")
# else:
#     print("Failed to retrieve draw results.")
