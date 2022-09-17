import logging
import json
from datetime import datetime, timedelta

from flask import request, jsonify

# from codeitsuisse import app

logger = logging.getLogger(__name__)

# @app.route('/calendarDays', methods=['POST'])
def evaluate_calendar():
    data = request.get_json()
    inputData = data.get('numbers')
    logging.info("data sent for evaluation {}".format(inputData))
    result = get_data_json(inputData)
    logging.info("My result :{}".format(result))
    return json.dumps(result)

def get_data_json(numbers: list) -> dict:
    output_dict = {}
    year = numbers[0]
    year_dates = YearDates(year)
    if len(numbers) > 1:
        days = sorted([day for day in numbers[1:] if day in range(1, year_dates.no_of_days+1)])
        part_1_string = process_days(days)
    elif len(numbers) == 1:
        part_1_string = "       ,       ,       ,       ,       ,       ,       ,       ,       ,       ,       ,       ,"
        part_2_list = [2001]
    output_dict['part1'] = part_1_string
    output_dict['part2'] = part_2_list
    return output_dict

def process_days(days: list) -> str:


def is_leap_year(year: int) -> bool:
    if year % 4 == 0:
        return True
    return False

class YearDates:
    def __init__(self, year: int):
        self.year = year
        self.no_of_days = 365 if not is_leap_year(year) else 366
        self.months = {}
        self.first_day = datetime(year, 1, 1).weekday()
        self.weekend_days = {0: (0, 6), 2: (5, 6), 3: (4, 5), 4: (2, 3), 5: (1, 2), 6: (0, 1)}
        self.first_weekend_day = self.weekend_days[self.first_day] # e.g. when Jan 1 is Friday, (2. 3)
        self.no_of_days = [31, 28 if not is_leap_year(year) else 29, 31, 30, 31, 30, 
                            31, 31, 30, 31, 30, 31]
        self.month_separating_dates = []
        self.current_day_index = 1
        for month in range(1, 13):
            weekdays = []
            weekends = []
            self.month_separating_dates.append(self.current_day_index)
            for day in range(self.current_day_index, self.current_day_index + self.no_of_days[month-1]):
                if any(day % 7 == self.first_weekend_day[i] for i in range(2)):
                    weekends.append(day)
                else:
                    weekdays.append(day)
            self.months[month] = {'weekdays': weekdays, 'weekends': weekends}
            self.current_day_index += self.no_of_days[month-1]

if __debug__:
    get_data_json([1])
    print