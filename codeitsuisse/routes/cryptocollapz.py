import logging
import json
import math

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/cryptocollapz', methods=['POST'])
def evaluate_crypto():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    inputLists = [l for l in data]
    result = []
    evaluator = PriceEvaluator()
    for l in inputLists:
        evaluator.routine = []
        outputList = evaluator.find_highest_price_list(l)
        result.append(outputList)
    logging.info("My result :{}".format(result))
    return json.dumps(result)

class PriceEvaluator:
    def __init__(self):
        self.price_dict = {}
        self.routine = []

    def find_highest_price_list(self, prices: list) -> list:
        highest_price_list = []
        for price in prices:
            highest_price_list.append(self.find_highest_price(price))
            self.routine = []
        return highest_price_list
    
    def find_highest_price(self, price: int, recursive=True) -> int:
        price = int(price)
        if int(price) not in self.routine:
            self.routine.append(int(price))
        if price in self.price_dict:
            return self.price_dict[price]
        # even no, max price of price / 2 is the same of max price of price, given price < max price
        elif price % 2 == 0 and price / 2 in self.price_dict and price < self.price_dict[price / 2]:
            self.price_dict[price] = self.price_dict[price / 2]
            return self.price_dict[price]
        # powers of 2
        elif math.log2(price) % 1 == 0 and price >= 4:
            self.price_dict[int(price)] = int(price)
            return int(price)
        # if the routine eventually arrived at a number smaller than the price, compare the max element
        # in the routine list with the highest price of the number
        elif price < self.routine[0] and recursive:
            if max(self.routine) > self.find_highest_price(price, recursive=False):
                self.price_dict[price] = max(self.routine)
                return max(self.routine)
            else:
                self.price_dict[price] = self.find_highest_price(price, recursive=False)
                return self.price_dict[price]
            # return self.find_highest_price(self.routine[0], recursive=False)
        # max of next price < first item in routine, return first item in routine
        elif price in self.price_dict and self.find_highest_price(price) < self.routine[0] and recursive:
            self.price_dict[self.routine[0]] = self.routine[0]
            return self.find_highest_price(self.routine[0], recursive=False)
        # even
        elif price % 2 == 0:
            return self.find_highest_price(price / 2)
        # odd
        else:
            return self.find_highest_price(price * 3 + 1)

if __debug__:
    evaluator = PriceEvaluator()
    print(evaluator.find_highest_price(999999999))