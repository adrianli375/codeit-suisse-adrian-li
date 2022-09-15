import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/tickerStreamPart2', methods=['POST'])
def evaluate():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    inputList = data.get("stream")
    quantityBlock = data.get("quantityBlock")
    resultList = {'output': to_cumulative_delayed(inputList, quantityBlock)}
    logging.info("My result :{}".format(resultList))
    return json.dumps(resultList)

def to_cumulative_delayed(stream: list, quantity_block: int) -> list:
    outList = []
    agg = dict()
    tickerList = dict()
    for i in stream:
        timestamp = int(i[:2]) * 60 + int(i[3:5])
        if timestamp not in agg:
            agg[timestamp] = dict()
        for a, b, c in zip(*([iter(i.split(",")[1:])] * 3)):
            agg[timestamp][a] = agg[timestamp].get(
                a, [0, 0])[0] + int(b), agg[timestamp].get(
                    a, [0, 0])[1] + oneDpToInt(c) * int(b)
            if a not in tickerList:
                tickerList[a] = [[0, 0], 0]
    for timeInfo, val in dict(sorted(agg.items())).items():
        res = ""
        for ticker, values in val.items():
            tickerList[ticker] = [[
                sum(x) for x in zip(tickerList[ticker][0], values)
            ], tickerList[ticker][1]]

            if tickerList[ticker][0][
                    0] >= tickerList[ticker][1] + quantity_block:
                tickerList[ticker][1] = tickerList[ticker][0][0] - \
                    tickerList[ticker][0][0] % quantity_block
                residueValue = values[1]//values[0] * \
                    (tickerList[ticker][0][0] % quantity_block)
                res += f",{ticker},{tickerList[ticker][1]},{intToOneDp(tickerList[ticker][0][1]-residueValue)}"
        if res:
            outList += [f"{timeInfo//60:02}:{timeInfo%60:02}" + res]
    return outList

def oneDpToInt(num: str) -> int:
    return int(num[:-2]) * 10 + int(num[-1])

def intToOneDp(num: int) -> str:
    return f"{num//10}.{num%10}"