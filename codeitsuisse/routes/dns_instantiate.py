import logging
import json
import pickle

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/instantiateDNSLookup', methods=['POST'])
def evaluate_lookup_table():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = process_table(data)
    logging.info("My result :{}".format(json.dumps(result)))
    return jsonify(result)

def process_table(data: dict):
    lookup_table = data['lookupTable']
    file = open('table.dat', 'wb')
    pickle.dump(lookup_table, file)
    file.close()
    return {'success': True}
