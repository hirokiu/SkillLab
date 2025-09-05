import os
import sounddevice as sd
import numpy as np
import time
from flask import Flask, render_template

app = Flask(__name__)

# データ保存用ディレクトリのパスを指定
data_directory = "/decibel_data"  # データを保存するディレクトリのパスを指定
data_file = "decibel_data.txt"  # データファイルの名前

if not os.path.exists(data_directory):
    os.makedirs(data_directory)

# しきい値を設定
threshold1 = 80  # 非常に混雑しています
threshold2 = 70  # 混雑しています
threshold3 = 60  # それほど混雑していません

# デシベルを測定する関数
def record_and_measure_decibel():
    duration = 10  # 10秒間録音
    sample_rate = 44100  # サンプルレート
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()
    decibel = 20 * np.log10(np.max(np.abs(recording)))  # デシベル測定方法は要調整

    with open(f"{data_directory}/{data_file}", "a") as file:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        file.write("{timestamp}: {decibel} dB\n")

@app.route("/")
def index():
    # ファイルから最新のデシベルデータを読み込み、混雑度合いを決定
    with open(f"{data_directory}/{data_file}", "r") as file:
        lines = file.readlines()
    if lines:
        latest_data = lines[-1].strip().split(": ")
        decibel = float(latest_data[1])
        if decibel > threshold1:
            congestion_level = "非常に混雑しています"
        elif decibel > threshold2:
            congestion_level = "混雑しています"
        elif decibel > threshold3:
            congestion_level = "それほど混雑していません"
        else:
            congestion_level = "混雑していません"
    else:
        congestion_level = "データがありません"
    
    return render_template("custom_templates/custom_index.html", congestion_level=congestion_level, latest_data=latest_data)


if __name__ == "__main__":
    # 5分ごとにデシベルを測定するためのループを実行
    while True:
        record_and_measure_decibel()
        time.sleep(300)  # 5分待つ
        app.run(debug=True)

