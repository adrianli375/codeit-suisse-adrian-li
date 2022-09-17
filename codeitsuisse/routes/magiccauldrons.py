import logging
import json
from datetime import datetime

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/calendarDays', methods=['POST'])
def evaluate_cauldrons():
    data = request.get_json()
    inputData = data.get()
    logging.info("data sent for evaluation {}".format(inputData))
    result = get_data_json(inputData)
    logging.info("My result :{}".format(result))
    return json.dumps(result)

def get_data_json(json_arrays):
    for testcase in json_arrays:
        