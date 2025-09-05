#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter import messagebox

import os
import sys
import requests
import time
import PySimpleGUI as sg
import webbrowser



api_key = 'NY2FZFYX7XOTZ41K'
read_key = 'VSRSCL53BN28BZ3F'
channle_id = '1500035'
data_file = "./data/cpu_temp.dat"

_ts_base_url = "https://api.thingspeak.com"
ts_update_url = _ts_base_url + "/update"
# GET https://api.thingspeak.com/update?api_key=MSUJ80Z21B6XIS7G&field1=0

# HTTPでのデータ登録のための設定
headers = {'X-THINGSPEAKAPIKEY': api_key}


#------
# powermetricsで取得したCPU die tempartureの値を取得して、配列を返す
# 引数：データが入ったファイルのパス
# return : cpu_temp リスト（配列）
# 2021-09-07T23:59:36 JST CPU die temperature: 69.77 C
#------
def getCpuTempFromFile(filename):

    _cpu_temps = []

    # ファイルの存在を確認
    is_file = os.path.exists(filename)
    if not is_file:
        print("正しいファイル名を指定してください。")
        sys.exit(1)

    # ファイルを開いてデータを取得
    with open(filename) as f:
        _lines = f.readlines()
        for _line in _lines:
            _data = _line.split()
            _cpu_temps.append(_data[5])
    
    return _cpu_temps

#------
# 指定したデータをThingSpeakに登録
# 引数：req_url, headers, post_data
#------
def post2ThingSpeak(req_url, headers, post_data):
    while True:
        response = requests.post(req_url, headers=headers, data=post_data)
        if response.text != '0':
            break
        time.sleep(1)


# メイン処理



def testScript():
    cpu_temps = []

    cpu_temps_av = []
    print(data_file + " のデータをThingSpeakに登録します。")
    # CPU温度の情報をファイルから取得
    cpu_temps = getCpuTempFromFile(data_file)
    k = 5



    for i in range (k):
        n = i * -1 +1
        temp = cpu_temps[n]
        f = float(temp)
        print(f)
        cpu_temps_av.append(f)

    print(cpu_temps_av)
    ave = 0
    ave = sum(cpu_temps_av)/len(cpu_temps_av)
    print(ave)

    if ave >= 95:
        messagebox.showinfo("確認", "CPUの温度平均" + str(ave) + "度を超えました" )



    post_data = {'field2': ave}
    post2ThingSpeak(ts_update_url, headers, post_data)


    print("CPU平均温度：" + str(ave) + " を登録しました。")


sg.theme('DarkAmber')   # デザインテーマの設定

# ウィンドウに配置するコンポーネント
layout = [  #[sg.Button('監視を起動')],
            [sg.Button('データ送信を起動'), sg.Button('表を表示'), sg.Button('終了')],
            [sg.Text('回数を選択'), sg.InputText()] ]

# ウィンドウの生成
window = sg.Window('CPU温度監視プログラム', layout)

# イベントループ
n = 1
while True:
    
    event, values = window.read()
    
    if event == sg.WIN_CLOSED or event == '終了':
        break
    elif event == 'データ送信を起動':
        n = int(values[0])
        for i in range(n):
            testScript()
            time.sleep(5)
    elif event == '監視を起動':
        import observer.py

    elif event == '表を表示':
        webbrowser.open('https://thingspeak.com/channels/1500035/charts/2?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&type=line&update=15')




sys.exit(0)
