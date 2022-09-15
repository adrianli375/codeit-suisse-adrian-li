import requests

# data = {'input': 3}
data = {'stream': ["00:06,A,1,5.6",
                    "00:05,A,1,5.6",
                    "00:00,A,1,5.6",
                    "00:02,A,1,5.6",
                    "00:03,A,1,5.6",
                    "00:04,A,1,5.6"], 
        'quantityBlock': 5}
headers = {'Content-type': 'application/json'}
request = requests.post(
    # 'https://codeit-suisse-adrian-li.herokuapp.com/square', 
    'https://codeit-suisse-adrian-li.herokuapp.com/tickerStreamPart2', 
                        json=data, headers=headers)
print(request.text)
print(request.status_code)
