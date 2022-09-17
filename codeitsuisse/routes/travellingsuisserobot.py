import logging
import json
import math
from datetime import datetime, timedelta

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/travelling-suisse-robot', methods=['POST'])
def evaluate_robot():
    data = request.get_data().decode("utf-8") 
    logging.info("data sent for evaluation {}".format(data))
    result = solve_robot(data)
    logging.info("My result :{}".format(json.dumps(result)))
    return result.encode("utf-8")

def solve_robot(map) -> str:
    start_time = datetime.now()
    locations_dict = {}
    # logging.info(map)
    # logging.info(f'Type of input: {type(map)}')
    map_rows_initialize = map.split('\n')
    map_rows = []
    for i in range(len(map_rows_initialize)):
        if map_rows_initialize[i] != '':
            map_rows.append(map_rows_initialize[i])
    row_index = 0
    for row in map_rows:
        if datetime.now() - start_time > timedelta(seconds=6.9):
            return 'SSSSSS'
        col_index = 0
        for entry in row:
            if entry != ' ':
                if entry not in locations_dict:
                    locations_dict[entry] = [(col_index, row_index)]
                else:
                    if locations_dict[entry] is not None:
                        temp = locations_dict[entry]
                        temp_list = []
                        for item in temp:
                            temp_list.append(item)
                        temp_list.append((col_index, row_index))
                        locations_dict[entry] = temp_list
                    else:
                        locations_dict[entry] = [(col_index, row_index)]
            col_index += 1
        row_index += 1
    start_coord = locations_dict['X']
    current_coord = start_coord[0]
    route = 'CODEITSUISSE'
    output_path = ''
    for item in route:
        if not any([item == letter for letter in ['E', 'I', 'S']]):
            item_coord = locations_dict[item][0]
        else:
            list_of_coord = locations_dict[item]
            shortest_index = 0
            index = 0
            dist = math.pow(2, 31) - 1
            for coord in list_of_coord:
                y_dist = coord[1] - current_coord[1]
                x_dist = coord[0] - current_coord[0]
                path_dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                if path_dist < dist:
                    dist = path_dist
                    shortest_index = index
                index += 1
            item_coord = locations_dict[item][shortest_index]
        x_dist = item_coord[0] - current_coord[0]
        y_dist = item_coord[1] - current_coord[1]

        if y_dist == 0:
            if x_dist > 0:
                output_path += 'R'
                for j in range(x_dist):
                    output_path += 'S'
                output_path += 'PL'
            elif x_dist < 0:
                output_path += 'L'
                for j in range(-x_dist):
                    output_path += 'S'
                output_path += 'PR'
        else:
            if y_dist < 0 and x_dist == 0:
                for j in range(-y_dist):
                    output_path += 'S'
                output_path += 'P'
            elif y_dist > 0 and x_dist == 0:
                output_path += 'RR'
                for j in range(y_dist):
                    output_path += 'S'
                output_path += 'PRR'
            elif y_dist < 0:
                if x_dist > 0:
                    for j in range(y_dist):
                        output_path += 'S'
                    output_path += 'R'
                    for j in range(x_dist):
                        output_path += 'S'
                    output_path += 'PL'
                elif x_dist < 0:
                    for j in range(y_dist):
                        output_path += 'S'
                    output_path += 'L'
                    for j in range(-x_dist):
                        output_path += 'S'
                    output_path += 'PR'
            elif y_dist > 0:
                if x_dist > 0:
                    output_path += 'RR'
                    for j in range(-y_dist):
                        output_path += 'S'
                    output_path += 'L'
                    for j in range(x_dist):
                        output_path += 'S'
                    output_path += 'PL'
                elif x_dist < 0:
                    output_path += 'RR'
                    for j in range(-y_dist):
                        output_path += 'S'
                    output_path += 'R'
                    for j in range(-x_dist):
                        output_path += 'S'
                    output_path += 'PR'

        for i in range(len(locations_dict[item])):
            if item_coord == locations_dict[item][i]:
                del locations_dict[item][i] 
                break
        current_coord = item_coord
    output = output_path.replace('RRR', 'L').replace('LLL', 'R').replace('RL', '').replace('LR', '')
    logging.info(output)
    return output
            
if __debug__:
    path = solve_robot('''
                                 \n
               D     E      I    \n
                                 \n
               O                 \n
                                 \n
               C            T    \n
                                 \n
               X                 \n
                                 \n
   E S   S       I     U    S    \n
                                 \n
''')
    print(path)