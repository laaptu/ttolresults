class DrawResult:
    def __init__(self, draw_number, draw_date, primary_numbers, secondary_numbers):
        self.draw_number = draw_number
        self.draw_date = draw_date
        self.primary_numbers = primary_numbers
        self.secondary_numbers = secondary_numbers

    def print(self):
        print("Draw Number:", self.draw_number)
        print("Draw Date:", self.draw_date)
        print("Primary Numbers:", self.primary_numbers)
        print("Secondary Numbers:", self.secondary_numbers)
        print()