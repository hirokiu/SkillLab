import time
import board
import adafruit_mpu6050
import csv
import os
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

# --- 設定 ---
# Firebaseの秘密鍵ファイル
CRED_PATH = 'your-firebase-credentials.json'
# Firebaseのコレクション名
COLLECTION_NAME = 'angle_data'
# ローカル保存するCSVファイル名
CSV_FILE = 'angle_log.csv'
# データ取得間隔（秒）
INTERVAL = 5

# --- Firebaseの初期化 ---
try:
    cred = credentials.Certificate(CRED_PATH)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print(" Firebaseの初期化に成功しました。")
except Exception as e:
    print(f" Firebaseの初期化に失敗: {e}")
    exit()

# --- センサーの初期化 ---
try:
    i2c = board.I2C()  # uses board.SCL and board.SDA
    mpu = adafruit_mpu6050.MPU6050(i2c)
    print(" MPU6050センサーの初期化に成功しました。")
except Exception as e:
    print(f" センサーの初期化に失敗: {e}")
    # ダミーモードで動作させるためのフラグ
    is_dummy_mode = True
    print(" センサーが見つからないため、ダミーデータで動作します。")
else:
    is_dummy_mode = False

# --- CSVファイルのヘッダー書き込み ---
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'x_angle', 'y_angle'])

# --- メインループ ---
def main():
    print(" データ収集を開始します...")
    while True:
        try:
            # タイムスタンプ取得
            now = datetime.now()
            timestamp_str = now.strftime('%Y-%m-%d %H:%M:%S')

            # 2. センサーから角度データを取得
            if is_dummy_mode:
                import random
                # 集中力が途切れる可能性のある値をランダムに生成
                x = random.uniform(-50, -10)
                y = random.uniform(-70, -30)
            else:
                # 実際のセンサーから値を取得 (MPU6050ライブラリは加速度を返すので、
                # 実際にはカルマンフィルタ等で角度に変換する処理が必要。ここでは簡略化)
                accel = mpu.acceleration
                # ここでは加速度のX, Yを角度に見立てて代入します
                x = accel[0] 
                y = accel[1]

            x_angle = round(x, 2)
            y_angle = round(y, 2)
            
            print(f"[{timestamp_str}] X: {x_angle}, Y: {y_angle}")

            # 3. Raspberry Pi上にローカル保存 (CSV)
            with open(CSV_FILE, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([timestamp_str, x_angle, y_angle])

            # 3. クラウドに保存 (Firestore)
            data = {
                'x_angle': x_angle,
                'y_angle': y_angle,
                'timestamp': firestore.SERVER_TIMESTAMP # クラウド側の正確な時刻を記録
            }
            db.collection(COLLECTION_NAME).add(data)

        except Exception as e:
            print(f"エラーが発生しました: {e}")
        
        time.sleep(INTERVAL)

if __name__ == '__main__':
    main()
