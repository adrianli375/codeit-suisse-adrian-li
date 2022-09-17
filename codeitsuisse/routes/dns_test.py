import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/test', methods=['POST'])
def evaluate_dns_test():
    data = {'teamUrl': 'https://codeit-suisse-adrian-li.herokuapp.com'}
    logging.info("data sent for evaluation {}".format(data))
    logging.info("My result :{}".format(json.dumps(data)))
    return jsonify(data)