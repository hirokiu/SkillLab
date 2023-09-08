import socket
import math
import requests

# Raspberry PiのIPアドレスとポート番号を設定
RASPBERRY_PI_IP = '10.50.79.124'
PORT = 12345  # 任意のポート番号

# 危険な場所までの距離の閾値（メートル単位）
DANGER_DISTANCE_THRESHOLD = 100

# 危険な場所の緯度と経度を指定
DANGER_LATITUDE = 35.000000  # 危険な場所の緯度を実際の値に置き換える
DANGER_LONGITUDE = 140.000000  # 危険な場所の経度を実際の値に置き換える

# LINE Notifyのアクセストークンを設定
ACCESS_TOKEN = 'sUO7PwlWVkpxxa40lMbSoCKJHrvt8Dzn85XqUpVnVZm'

# Raspberry Piのソケットを作成
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((RASPBERRY_PI_IP, PORT))
server_socket.listen(1)  # 1つの接続を待機

print("Raspberry PiがiPhoneからの接続を待機しています...")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"iPhoneが{client_address}から接続しました")

    # iPhoneから位置情報データを受信
    data = client_socket.recv(1024).decode('utf-8')
    print(f"受信したデータ: {data}")

    # 位置情報データの解析（例：緯度と経度を取得）
    try:
        latitude, longitude = map(float, data.split(','))
        print(f"緯度: {latitude}, 経度: {longitude}")

        # 危険な場所までの距離を計算
        # ここでは簡易的な直線距離を計算していますが、より正確な方法を使用することができます。
        distance = math.sqrt((latitude - DANGER_LATITUDE)**2 + (longitude - DANGER_LONGITUDE)**2)

        if distance <= DANGER_DISTANCE_THRESHOLD:
            print("危険な場所に近づいています！警告を発信します。")
            
            # LINE Notifyに通知を送信
            message = '危険な場所に近づいています。'
            url = 'https://notify-api.line.me/api/notify'
            headers = {
                'Authorization': f'Bearer {ACCESS_TOKEN}',
            }
            data = {
                'message': message,
            }
            response = requests.post(url, headers=headers, data=data)
            
            if response.status_code == 200:
                print('LINE Notifyへの通知を送信しました')
            else:
                print('LINE Notifyへの通知の送信に失敗しました')
        else:
            print("安全です。")

    except ValueError:
        print("位置情報データの解析に失敗しました。")

    client_socket.close()

# ソケットをクローズ
server_socket.close()
