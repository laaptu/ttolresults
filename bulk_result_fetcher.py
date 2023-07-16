from datetime import datetime
from db_connector import DBConnector
from draw_result import DrawResult
from frequency import Frequency
from result_fetcher import get_draw_results

class BulkResultFetcher:
    def __init__(self):
        self.db_connector = DBConnector()

    def fetch_bulk_result(self):
        current_year = datetime.now().year
        for year in range(2014, current_year + 1):
            for month in range(1, 13):
                date = datetime(year, month, 1)  # First day of the month
                frequency = Frequency.MONTHLY
                draw_results = get_draw_results(date, frequency)
                self.process_draw_results(draw_results, date)  

    def get_current_month_result(self):
        date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)  # First day of the month
        frequency = Frequency.MONTHLY
        draw_results = get_draw_results(date, frequency)
        self.process_draw_results(draw_results, date)                                  
                

    def process_draw_results(self, draw_results, date):
        if draw_results:
            for result in draw_results:
                result.print()  # Print each draw_result
                print()  # Add a newline for readability                 
            self.db_connector.save_draw_results(draw_results)
            print(f"DrawResults for {date.strftime('%B %Y')} saved successfully!")    
        else:
            print(f"Failed to retrieve draw results for {date.strftime('%B %Y')}.")    

# Usage example
bulk_fetcher = BulkResultFetcher()
bulk_fetcher.get_current_month_result()
