import logging
import json
import math

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/quordleKeyboard', methods=['POST'])
def evaluate_keyboard():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = process_answer(data)
    logging.info("My result :{}".format(json.dumps(result)))
    return jsonify(result)

def process_answer(data: dict) -> dict:
    answers = data['answers']
    attempts = data['attempts']
    numbers = data['numbers']
    part1_ans, unused_letters = get_part1_answer(answers, attempts)
    part2_ans = get_part2_answer(part1_ans, unused_letters, numbers)
    result_dict = {'part1': part1_ans, 'part2': part2_ans}
    return result_dict

def get_part1_answer(answers: list, attempts: list):
    no_of_attempts = len(attempts)
    letters_dict = {}
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        letters_dict[letter] = 0
    ans_letter_count = {}
    for answer in answers:
        for char in answer:
            if char not in ans_letter_count:
                ans_letter_count[char] = 1
            else:
                ans_letter_count[char] = ans_letter_count[char] + 1
    
    for attempt in attempts:
        if attempt in answers:
            for char in attempt:
                if ans_letter_count[char] == 1:
                    del ans_letter_count[char]
                else:
                    ans_letter_count[char] = ans_letter_count[char] - 1
        
        list_of_chars = []
        for char in attempt:
            if char not in list_of_chars:
                list_of_chars.append(char)
        
        for char in list_of_chars:
            if char not in ans_letter_count and letters_dict[char] == 0:
                letters_dict[char] = no_of_attempts
        no_of_attempts -= 1
    output_no_string = ''
    unused_letters = ''
    for char in letters_dict:
        if letters_dict[char] == 0:
            unused_letters += char
        else:
            output_no_string += str(letters_dict[char])
    return output_no_string, unused_letters

def get_part2_answer(output_string: str, unused_chars: str, numbers: list) -> str:
    num_entries = []
    output = ''
    for i in range(5):
        num_entries.append(numbers[5*i:5*(i+1)])
    for sublist in num_entries:
        binary_list = []
        for num in sublist:
            if str(num) in output_string:
                binary_list.append(1)
            else:
                binary_list.append(0)
        binary_rep = get_decimal_from_binary(binary_list)
        char = chr(binary_rep + 64)
        output += char
    for char in unused_chars:
        if char not in output:
            output += unused_chars
    return output

def get_decimal_from_binary(l: list) -> int:
    result = 0
    power = len(l) - 1
    for i in range(len(l)):
        if l[i] == 1:
            result += l[i] * math.pow(2, power)
        power -= 1
    return int(result)

if __debug__:
    output, unused = get_part1_answer(
        ['VVIDH', 'MZLPS', 'BPCYN', 'XYGGM'], 
        ['JKGJB', 'ZGRUJ', 'XYGGM', 'BPCYN', 'MHXGE', 'DZENT', 'ZXWQW', 'VVIDH', 'MZLPS']
    )
    print(output)
    print(unused)
    part_2_ans = get_part2_answer(output, unused, 
    [761, 720, 13, 750, 936, 237, 482, 609, 585, 706, 240, 23, 76, 61, 700, 711, 823, 406, 376, 455, 818, 482, 338, 572, 257])
    print(part_2_ans)