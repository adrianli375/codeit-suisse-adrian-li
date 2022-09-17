import requests

# data = {'input': 3}
# data = {'stream': ["00:06,A,1,5.6",
#                     "00:05,A,1,5.6",
#                     "00:00,A,1,5.6",
#                     "00:02,A,1,5.6",
#                     "00:03,A,1,5.6",
#                     "00:04,A,1,5.6"], 
#         'quantityBlock': 5}
data = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]
headers = {'Content-type': 'application/json'}
request = requests.post(
    # 'https://codeit-suisse-adrian-li.herokuapp.com/square', 
    # 'https://codeit-suisse-adrian-li.herokuapp.com/tickerStreamPart2', 
    'https://codeit-suisse-adrian-li.herokuapp.com/cryptocollapz', 
                        json=data, headers=headers)
print(request.text)
print(request.status_code)
