import sqlite3
from draw_result import DrawResult

class DBConnector:
    def __init__(self, db_name='draw_results.db'):
        self.db_name = db_name

    def save_draw_results(self, draw_results):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS draw_results (
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

            cursor.execute('INSERT OR REPLACE INTO draw_results VALUES (?, ?, ?, ?)', data)

        conn.commit()
        conn.close()

    def get_all_draw_results(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM draw_results ORDER BY draw_date DESC')
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
