# CSVファイルを読み込む
with open('csn.log', 'r') as file:
    lines = file.readlines()

timestamps = []
x_accelerations = []
y_accelerations = []
z_accelerations = []

for line in lines:
    parts = line.split(",")  # スペースで行を分割
    if len(parts) == 4:  # タイムスタンプと3軸の加速度データがある場合
        timestamp = float(parts[0])
        x_acceleration = float(parts[1])
        y_acceleration = float(parts[2])
        z_acceleration = float(parts[3])
        timestamps.append(timestamp)
        x_accelerations.append(x_acceleration)
        y_accelerations.append(y_acceleration)
        z_accelerations.append(z_acceleration)

from datetime import datetime

# UNIX時間を日付と分までの時間に変換
converted_timestamps = [datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S') for timestamp in timestamps]

# 変化を検出するための閾値
threshold = 1.0  # 例: 1.0とし、必要に応じて調整

# 変化が大きいタイムスタンプを格納するリスト
significant_changes_x = []
significant_changes_y = []

# 最後に変化が検出されたタイムスタンプ
last_change_x = None
last_change_y = None

# 加速度データのインデックス0からlen(y_accelerations)-2までループ
for i in range(len(y_accelerations) - 1):
    # 現在のデータ点と次のデータ点の差分を計算
    acceleration_change_x = abs(x_accelerations[i] - x_accelerations[i + 1])
    acceleration_change_y = abs(y_accelerations[i] - y_accelerations[i + 1])
    
    # 変化が閾値を超える場合、かつ直近の変化から15秒以上の間隔がある場合、タイムスタンプをリストに追加
    if acceleration_change_x > threshold and (last_change_x is None or timestamps[i + 1] - last_change_x >= 15):
        significant_changes_x.append(converted_timestamps[i + 1])
        last_change_x = timestamps[i + 1]
    if acceleration_change_y > threshold and (last_change_y is None or timestamps[i + 1] - last_change_y >= 15):
        significant_changes_y.append(converted_timestamps[i + 1])
        last_change_y = timestamps[i + 1]

# 変化が大きいタイムスタンプを出力
print("Significant Changes in X Acceleration:")
for timestamp in significant_changes_x:
    print(timestamp)

print("\nSignificant Changes in Y Acceleration:")
for timestamp in significant_changes_y:
    print(timestamp)
