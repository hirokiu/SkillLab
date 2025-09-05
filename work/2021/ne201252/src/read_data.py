import requests
import time
from time import sleep

api_key = 'Z4KUE29S2KHYR8MH'
url = 'https://api.thingspeak.com/channels/1501319/fields/1.json'
#channle_id = '1501319'

#_ts_base_url = "https://api.thingspeak.com"
#ts_fields_url = _ts_base_url + "/fields/1.json"
# GET https://api.thingspeak.com/channels/1501319/fields/1.json?api_key=Z4KUE29S2KHYR8MH&results=2

def rec_data():
    response = requests.get(url,
        params = {
            'api_key': api_key,
            'timezone': 'Asia/Tokyo',
            'results': 1
        })
    for i in range(0, 100, 1):
        time.sleep(15)
        response_list = response.json()['feeds']
        data = []
        for elm in response_list:
            data.append(elm['field1'])
       # print(response_list)
        print(data)

def main_loop():
    rec_data()

if __name__ == '__main__':
    main_loop()
