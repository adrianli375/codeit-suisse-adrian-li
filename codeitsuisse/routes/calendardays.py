from calendar import month
import logging
import json
from datetime import datetime, timedelta

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/calendarDays', methods=['POST'])
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
        part_1_string = year_dates.process_days(days)
        part_2_list = generate_year_list(part_1_string)
    elif len(numbers) == 1:
        part_1_string = "       ,       ,       ,       ,       ,       ,       ,       ,       ,       ,       ,       ,"
        part_2_list = [2001]
    output_dict['part1'] = part_1_string
    output_dict['part2'] = part_2_list
    return output_dict

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
        self.weekend_days = {0: (0, 6), 1: (5, 6), 2: (4, 5), 3: (3, 4), 4: (2, 3), 5: (1, 2), 6: (0, 1)}
        self.weekday_days = {0: (1, 2, 3, 4, 5), 1: (0, 1, 2, 3, 4), 2: (0, 1, 2, 3, 6), 3: (0, 1, 2, 5, 6), 
                            4: (0, 1, 4, 5, 6), 5: (0, 3, 4, 5, 6), 6: (2, 3, 4, 5, 6)}
        self.first_weekend_day = self.weekend_days[self.first_day] # e.g. when Jan 1 is Friday, (2. 3)
        self.first_weekday_day = self.weekday_days[self.first_day] # e.g. when Jan 1 is Friday, (0, 1, 4, 5, 6)
        self.no_of_days_list = [31, 28 if not is_leap_year(year) else 29, 31, 30, 31, 30, 
                                31, 31, 30, 31, 30, 31]
        self.month_separating_dates = []
        self.current_day_index = 1
        for month in range(1, 13):
            weekdays = []
            weekends = []
            self.month_separating_dates.append(self.current_day_index)
            for day in range(self.current_day_index, self.current_day_index + self.no_of_days_list[month-1]):
                if any(day % 7 == self.first_weekend_day[i] for i in range(2)):
                    weekends.append(day)
                else:
                    weekdays.append(day)
            self.months[month] = {'weekdays': weekdays, 'weekends': weekends}
            self.current_day_index += self.no_of_days_list[month-1]
        self.month_separating_dates.append(self.no_of_days+1)
    
    def all_days_included(self, month_day_list: list, mode='all') -> bool:
        '''mode: all, weekday or weekend'''
        if mode == 'all':
            decider = [False for i in range(7)]
            for day in month_day_list:
                decider[day % 7] == True
                if decider == [True for i in range(7)]:
                    return True
            return False
        
        elif mode == 'weekday':
            decider = [False for i in range(5)]
            for day in month_day_list:
                for i in range(5):
                    if day % 7 == self.first_weekday_day[i]:
                        decider[i] = True
                    if decider == [True for i in range(5)]:
                        return True
            return False
        
        elif mode == 'weekend':
            decider = [False for i in range(2)]
            for day in month_day_list:
                for i in range(2):
                    if day % 7 == self.first_weekend_day[i]:
                        decider[i] = True
                    if decider == [True for i in range(2)]:
                        return True
            return False
    
    def process_days(self, days: list) -> str:
        output_str = ''
        
        for i in range(12):
            month_output_str = ''
            month_day_list = [day for day in days if day in range(self.month_separating_dates[i], self.month_separating_dates[i+1])]
            month_weekend_list = self.months[i+1]['weekends']
            month_weekday_list = self.months[i+1]['weekdays']

            if self.all_days_included(month_day_list, mode='all'):
                month_output_str = 'alldays,'
            
            elif all([day in month_weekend_list for day in month_day_list]) and self.all_days_included(month_day_list, mode='weekend'):
                month_output_str = 'weekend,'
            
            elif all([day in month_weekday_list for day in month_day_list]) and self.all_days_included(month_day_list, mode='weekday'):
                month_output_str = 'weekday,'

            else:
                days_of_the_week = '01234560123456'

                date_mapping = {} # e.g. 0: '4', 1: '5', 2: '6', 3: '0', 4: '1', 5: '2', 6: '3'
                for date in range(0, 7):
                    date_mapping[date] = days_of_the_week[self.first_day + date - 1]
                
                date_string_mapping = {0: 'm', 1: 't', 2: 'w', 3: 't', 4: 'f', 5: 's', 6: 's'}
                month_output_str_list = [' ' for i in range(7)]

                for i in range(len(month_day_list)):
                    date_index = date_mapping[month_day_list[i] % 7]
                    month_output_str_list[int(date_index)] = date_string_mapping[int(date_index)]
                # string concatenation
                month_output_str_list.append(',')
                for string in month_output_str_list:
                    month_output_str += string
                if month_output_str == 'mtwtfss,':
                    month_output_str = 'alldays,'
            output_str += month_output_str
        return output_str
    
def generate_year_list(generated_string: str) -> list:
    output_list = []
    months_requirement = generated_string.split(',')
    derived_year = 2001 + generated_string.find(' ')
    year_date_derived = YearDates(derived_year)
    output_list.append(derived_year)
    for i in range(12):
        current_month = i + 1
        month_str = months_requirement[i]
        if month_str == 'alldays' or month_str == 'weekday':
            for j in range(5):
                output_list.append(year_date_derived.months[current_month]['weekdays'][j])
        elif month_str == 'alldays' or month_str == 'weekend':
            for j in range(2):
                output_list.append(year_date_derived.months[current_month]['weekends'][j])
        else:
            for j in range(7):
                dates = list(range(year_date_derived.month_separating_dates[i], 
                                    year_date_derived.month_separating_dates[i+1]))
                if month_str[j] != ' ':
                    division_remainder = (7 - year_date_derived.first_day + j + 1) % 7
                    for k in dates:
                        if k % 7 == division_remainder:
                            output_list.append(k)
                            break
    return output_list



if __debug__:
    get_data_json([2053, 274, 57, 306, 330, 245, 213, 277, 5, 334, 304, 38, 246, 178, 247, 868, 153, 185, 248, 280, 123, 219, 241, 34, 181, 151, -86, 84, 310, 240, 788, 145, 219, 307, 302, 268, 96, 183, 976, 35, 269, 308, 154, 276, 157, 303, 994, 156, 124, 64, 308, 175, 64, 63, 38, 188, 276, 25, 154, 662, 332, 157, 34, 4, 300, 209, 298, 116, 123, -33, 4, 402, 303, 305, 85, 490, 244, 247, 331, 185, 153, 85, -41, 307, 958, 34, -33, 333, 55, 920, 123, 176, 309, 247, 279, 86, 156, 157, 961, 248, 183, 95, 309, 310, 36, -79, 56, 311, 65, 278, 211, 305, 245, 244, 96, 213, -41, 275, -17, 280, 306, 26, 273, 307, -17, 219, -23, 59, 299, 185, -68, 279, -32, 117, 63, 246, 188, 947, 206, 5, 278, 26, 65, 739, 124, 58, 95, 328, 274, 177, 275, 267, 37, 96, 155, 35, 36, 37, 155, -19, 329, 301, 272, 311, 277])
