import logging
import json
import math

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/stig/warmup', methods=['POST'])
def evaluate_stig_warmup():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = process_interviews(data)
    logging.info("My result :{}".format(json.dumps(result)))
    return jsonify(result)

def process_interviews(interviews: list) -> list:
    output_list = []
    for interview in interviews:
        accuracy = get_p_q_value(interview)
        output_list.append(accuracy)

def get_p_q_value(interview: dict) -> dict:
    lower = interview['questions']['lower']
    higher = interview['questions']['higher']
    max_rating = interview['maxRating']
    if lower == 1:
        p = lower
        q = max_rating
    else:
        p = 2
        q = max_rating
    gcd = math.gcd(p, q)
    p /= gcd
    q /= gcd
    return {'p': p, 'q': q}
    
