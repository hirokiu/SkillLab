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
converted_timestamps = [datetime.utcfromtimestamp(timestamp).strftime('%d %H:%M:%S') for timestamp in timestamps]

import matplotlib.pyplot as plt

plt.figure(figsize=(12, 8))
plt.plot(converted_timestamps, x_accelerations, label='X Acceleration', linestyle='-')
plt.plot(converted_timestamps, y_accelerations, label='Y Acceleration', linestyle='-')
# plt.plot(converted_timestamps, z_accelerations, label='Z Acceleration')

plt.xlabel('Timestamp')
plt.ylabel('Acceleration')
plt.title('Acceleration Data')
plt.ylim(-1.5,4.0)
plt.yticks([-1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]) # y軸の詳細な刻み幅を設定
plt.legend()
plt.grid(True)
plt.xticks([]) #非表示
plt.show()
