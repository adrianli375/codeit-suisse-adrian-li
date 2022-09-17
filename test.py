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
[2082, 121, 798, 309, 37, 307, 64, 238, 185, 272, 277, 276, 119, 3, 332, 339, -87, -97, 361, 215, 93, 310, 127, 183, 124, 218, 176, 96, 60, 244, 66, 151, -47, 878, 58, 240, 33, 177, 147, 175, 420, 219, 126, 237, 85, 36, 305, 308, 217, 96, 239, 310, 57, 183, 157, 153, 97, -48, 6, 330, 329, 92, 306, 148, -17, 216, 153, -9, 311, 38, 94, 63, 912, 950, 86, 180, 117, 95, 35, 152, 36, 243, 150, 37, 114, 120, 311, 6, 127, 157, 64, 153, 277, 91, 124, 244, 125, 145, 154, 156, 60, 306, 92, 311, 4, 61, 155, 4, 122, 158, 188, 334, 298, 37, 65, 28, 218, 155, 59, 116, 94, 38, 154, 31, 148, 217, 305, 118, 188, 185, 339, 178, 728, 152, 340, 328, -12, 62, 97, 805, 65, 54, 7, 7, 84, 179, 309, 95, 268, 33, 126, 304, 122, 360, 27, 35, 333, 217, -29, 247, -90, 244, 340, 219, 3, 88, 121, 123, 706, 92, 307, 32, 211, 146, 90, 55, 276, 156, 125, 331, 89, 25, 34, -3, 449, 185, 340, 53, 216, 308, 93, 866, 34, 3, 206, 247, 56, 91, 32, 181, -41, 63, 66, 61, 215, 66, 451, 115, 62, 158, 276, 87, -51, 123, 209, 803, 149]}
headers = {'Content-type': 'application/json'}
request = requests.post(
    # 'https://codeit-suisse-adrian-li.herokuapp.com/square', 
    # 'https://codeit-suisse-adrian-li.herokuapp.com/tickerStreamPart2', 
    # 'https://codeit-suisse-adrian-li.herokuapp.com/cryptocollapz', 
    'https://codeit-suisse-adrian-li.herokuapp.com/calendarDays', 
                        json=data, headers=headers)
print(request.text)
print(request.status_code)
