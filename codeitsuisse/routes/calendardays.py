import logging
import json
from datetime import datetime, timedelta

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/calendardays', methods=['POST'])
def evaluate_calendar():
    data = request.get_json()
    inputData = data.get('numbers')
    logging.info("data sent for evaluation {}".format(inputData))
    result = get_data_json(inputData)
    logging.info("My result :{}".format(result))
    return json.dumps(result)

def get_data_json(numbers: list) -> dict:
    year = numbers[0]
    year_dates = YearDates(year)

    pass

class YearDates:
    def __init__(self, year: int):
        self.year = year
        self.no_of_days = 365 if not is_leap_year(year) else 366
        self.months = {}
        for i in range(1, 13):
            self.months

def is_leap_year(year: int) -> bool:
    if year % 4 == 0:
        return True
    return False