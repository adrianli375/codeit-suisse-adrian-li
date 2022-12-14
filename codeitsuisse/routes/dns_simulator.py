import logging
import json
import pickle

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/simulateQuery', methods=['POST'])
def evaluate_simulation():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = process_results(data)
    logging.info("My result :{}".format(json.dumps(result)))
    return jsonify(result)

def process_results(data: dict) -> list:
    cache_size = data['cacheSize']
    queries = data['log']
    output = get_status(cache_size, queries)
    return output

def get_status(size: int, queries: dict) -> list:
    file = open('table.dat', 'rb')
    lookup_table = pickle.load(file)
    output_list = []
    cache = {}
    cache_recent_query = {}
    time = 1

    for query in queries:
        if query not in cache and query in lookup_table:
            status = 'cache miss'
            ip_address = lookup_table[query]
            if len(cache) == size:
                last_time = min([q for q in cache_recent_query.keys() if cache_recent_query[q] in cache])
                least_visited_query = cache_recent_query[last_time]
                logging.info(f'recent queries: {cache_recent_query}')
                logging.info(f'cache: {cache}')
                logging.info(f'deleting {least_visited_query}')
                del cache[least_visited_query]
            cache[query] = lookup_table[query]
            if query in cache_recent_query.values():
                min_timestamp = [t for t in cache_recent_query.keys() if cache_recent_query[t] == query][0]
                del cache_recent_query[min_timestamp]
            cache_recent_query[time] = query
        elif query in cache and query in lookup_table:
            status = 'cache hit'
            ip_address = lookup_table[query]
            cache[query] = lookup_table[query]
            for i in cache_recent_query.keys():
                if cache_recent_query[i] == query:
                    del cache_recent_query[i]
                    break
            cache_recent_query[time] = query
        else:
            status = 'invalid'
            ip_address = None
        
        output_list.append({'status': status, 'ipAddress': ip_address})
        time += 1
    return output_list
