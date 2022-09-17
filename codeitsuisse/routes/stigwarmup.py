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

def process_interviews(data: list) -> list:
    output_list = []
    interviews = data[0]['questions']
    max_rating = data[0]['maxRating']
    for interview in interviews:
        accuracy = get_p_q_value(interview, max_rating)
        output_list.append(accuracy)
    return output_list

def get_p_q_value(interview: dict, max_rating: int) -> dict:
    logging.info(interview.keys())
    lower = interview['lower']
    if lower == 1:
        p = lower
        q = max_rating
    else:
        p = 2
        q = max_rating
    gcd = math.gcd(p, q)
    p /= gcd
    q /= gcd
    return {'p': int(p), 'q': int(q)}
    
if __debug__:
    result = process_interviews([{
   "questions": [{
      "lower": 2,
      "upper": 3
   }],
   "maxRating": 5
}])
    print(result)