import logging
import json
import math

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/magiccauldrons', methods=['POST'])
def evaluate_cauldrons():
    data = request.get_json()
    inputData = data.get()
    logging.info("data sent for evaluation {}".format(inputData))
    result = get_data_json(inputData)
    logging.info("My result :{}".format(result))
    return jsonify(result)

def get_data_json(json_arrays: list) -> list:
    output_list = []
    for testcase in json_arrays:
        result_dict = {}
        part_1_dict = testcase['part1']
        part_1_ans = get_amount_of_soup_1(part_1_dict)
        result_dict['part1'] = part_1_ans
        part_2_dict = testcase['part2']
        part_2_ans = get_time_2(part_2_dict)
        result_dict['part2'] = part_2_ans
        part_3_dict = testcase['part3']
        part_3_ans = 0
        result_dict['part3'] = part_3_ans
        part_4_dict = testcase['part4']
        part_4_ans = 0
        result_dict['part4'] = part_4_ans
        output_list.append(result_dict)
    return output_list


def get_amount_of_soup_1(soup_dict: dict) -> float:
    flow_rate = float(soup_dict['flow_rate'])
    time = int(soup_dict['time'])
    row_no = int(soup_dict['row_number'])
    col_no = int(soup_dict['col_number'])

    vol_soup = flow_rate * time
    time_to_fill_up_one = 100 / flow_rate
    current_level = time // time_to_fill_up_one

    if row_no > current_level:
        return float(round(0, 2))
    elif row_no < current_level:
        return float(round(100, 2))
    else:
        amount_flown = flow_rate * (time - time_to_fill_up_one * (row_no+1) * row_no / 2)
        if col_no == 0 or col_no == 0:
            if row_no != 0:
                return float(round(1/(2*row_no) * amount_flown, 2))
            else:
                return float(round(amount_flown, 2))
        else:
            if row_no != 0:
                return float(round(2/(2*row_no) * amount_flown, 2))
            else:
                return float(round(amount_flown, 2))

def get_time_2(soup_dict: dict) -> int:
    flow_rate = float(soup_dict['flow_rate'])
    amount_of_soup = float(soup_dict['amount_of_soup'])
    row_no = int(soup_dict['row_number'])
    col_no = int(soup_dict['col_number'])
    if row_no == 0 and col_no == 0:
        return round_float(amount_of_soup / flow_rate)
    elif col_no == 0 or col_no == row_no:
        edge_flow_rate = flow_rate / math.pow(2, row_no)
        return round_float(amount_of_soup / edge_flow_rate)
    else:
        new_flow_rate = 2 * flow_rate / math.pow(2, row_no)
        return round_float(amount_of_soup / new_flow_rate)

def round_float(f: float) -> int:
    if f % 1 == 0:
        return int(f)
    elif not f % 0.5 == 0:
        return int(round(f))
    else:
        int_part = f - 0.5
        if int_part % 2 == 0:
            return int_part
        else:
            return int_part + 1

if __debug__:
    amount = get_amount_of_soup_1({'flow_rate': 23, 'time': 1, 'row_number': 0, 'col_number': 0})
    print