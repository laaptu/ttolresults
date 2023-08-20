import sqlite3
from draw_result import DrawResult
from lott import Lott

class DBConnector:
    def __init__(self, db_name='draw_results.db'):
        self.db_name = db_name

    def save_draw_results(self, draw_results, lott):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        table_name = self.get_table_name(lott)

        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                draw_number INTEGER,
                draw_date TEXT UNIQUE,
                primary_numbers TEXT,
                secondary_numbers TEXT
            )
        ''')

        for result in draw_results:
            data = (
                result.draw_number,
                result.draw_date,
                ','.join(map(str, result.primary_numbers)),
                ','.join(map(str, result.secondary_numbers))
            )

            cursor.execute(f'INSERT OR REPLACE INTO {table_name} VALUES (?, ?, ?, ?)', data)

        conn.commit()
        conn.close()

    def get_table_name(self, lott):
        return lott.name

    def get_all_draw_results(self, lott):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        table_name = get_table_name(lott)
        cursor.execute(f'SELECT * FROM {table_name} ORDER BY draw_date DESC')
        rows = cursor.fetchall()

        draw_results = []
        for row in rows:
            draw_number, draw_date, primary_numbers_str, secondary_numbers_str = row
            primary_numbers = list(map(int, primary_numbers_str.split(',')))
            secondary_numbers = list(map(int, secondary_numbers_str.split(',')))
            draw_result = DrawResult(draw_number, draw_date, primary_numbers, secondary_numbers)
            draw_results.append(draw_result)

        conn.close()

        return draw_results    
