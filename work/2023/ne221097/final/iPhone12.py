# iPhoneから位置情報を取得し、ThingSpeakにデータを送信するスクリプト

import requests
import json
import time

# ThingSpeakのAPIキーとチャンネルID
api_key = 'D0Y5W56XFD1BO4D6'
channel_id = '2262981'

# ThingSpeakにデータを送信する関数
def send_data_to_thingspeak(latitude, longitude):
    url = f'https://api.thingspeak.com/update?api_key={api_key}&field1={latitude}&field2={longitude}'
    response = requests.get(url)
    if response.status_code == 200:
        print('Data sent to ThingSpeak successfully')
    else:
        print('Failed to send data to ThingSpeak')

# 位置情報を取得する関数（iPhoneからのデータを想定）
def get_location_data():
    # 仮の位置情報を生成（実際にはiPhoneから取得）
    latitude = 37.7749
    longitude = -122.4194
    return latitude, longitude

while True:
    latitude, longitude = get_location_data()
    send_data_to_thingspeak(latitude, longitude)
    time.sleep(60)  # 60秒ごとにデータを送信
