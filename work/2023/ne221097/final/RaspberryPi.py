# Raspberry Pi上でThingSpeakからデータを受信し、危険な場所に近づいたかどうかを判断するスクリプト

import requests

# ThingSpeakのチャンネルIDとAPIキー
channel_id = '2262981'
api_key = 'D0Y5W56XFD1BO4D6'

# Line通知用の関数
def send_line_notification(message):
    # ここにLine通知のコードを追加（LineのAPIを使用する必要があります）

# ThingSpeakからデータを取得する関数
def get_data_from_thingspeak():
    url = f'https://api.thingspeak.com/channels/{channel_id}/feeds.json?api_key={api_key}&results=1'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'feeds' in data and len(data['feeds']) > 0:
            return data['feeds'][0]
    return None

# 危険な場所に近づいたかどうかを判断する関数
def check_for_dangerous_location(latitude, longitude):
    # ここに危険な場所の判定ロジックを追加
    # 例えば、特定の座標が危険な場所であると判断した場合に警告を出す処理を行う

while True:
    data = get_data_from_thingspeak()
    if data:
        latitude = float(data['field1'])
        longitude = float(data['field2'])
        if check_for_dangerous_location(latitude, longitude):
            send_line_notification('危険な場所に近づきました！')
    time.sleep(60)  # 60秒ごとにThingSpeakからデータを取得

