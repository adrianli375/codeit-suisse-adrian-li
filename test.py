import requests

# data = {'input': 3}
# data = {'stream': ["00:06,A,1,5.6",
#                     "00:05,A,1,5.6",
#                     "00:00,A,1,5.6",
#                     "00:02,A,1,5.6",
#                     "00:03,A,1,5.6",
#                     "00:04,A,1,5.6"], 
#         'quantityBlock': 5}
# data = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]
data = {"numbers": 
[2036,5,6,38,33,63,65,67,61,98,92,95,97,127,122,123,124,125,154,159,184,186,187,220,214,215,216,246,250,280,281,275,277,278,308,309,310,311,312,306,336,337,338,339,342]}
headers = {'Content-type': 'application/json'}
request = requests.post(
    # 'https://codeit-suisse-adrian-li.herokuapp.com/square', 
    # 'https://codeit-suisse-adrian-li.herokuapp.com/tickerStreamPart2', 
    # 'https://codeit-suisse-adrian-li.herokuapp.com/cryptocollapz', 
    'https://codeit-suisse-adrian-li.herokuapp.com/calendarDays', 
                        json=data, headers=headers)
print(request.text)
print(request.status_code)
