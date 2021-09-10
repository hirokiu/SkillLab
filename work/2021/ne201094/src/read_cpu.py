#!/usr/bin/env python
# -*- coding: utf-8 -*-

import schedule
import time
import os
import sys
import requests
import send_gmail

api_key = 'WTGI0O7CXY05SR6M'
channle_id = '1501473'
data_file = "./data/cpu_temp.dat"
data_file_capa_cur = "./data/capa_cur.dat"
data_file_capa_max = "./data/capa_max.dat"
data_file_light = "./data/light.dat"

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
def job():
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

    def getCurrentCapa(data_file_capa_cur):
        _cur_temps = []

        # ファイルの存在を確認
        is_file = os.path.exists(data_file_capa_cur)
        if not is_file:
            print("正しいファイル名を指定してください。")
            sys.exit(1)

        # ファイルを開いてデータを取得
        with open(data_file_capa_cur) as f:
            _lines = f.readlines()
            for _line in _lines:
                _data = _line.split()
                _cur_temps.append(_data[4])

        return _cur_temps


    def getMaxCapa(data_file_capa_max):
        _max_temps = []

        # ファイルの存在を確認
        is_file = os.path.exists(data_file_capa_max)
        if not is_file:
            print("正しいファイル名を指定してください。")
            sys.exit(1)

        # ファイルを開いてデータを取得
        with open(data_file_capa_max) as f:
            _lines = f.readlines()
            for _line in _lines:
                _data = _line.split()
                _max_temps.append(_data[4])

        return _max_temps

    def getLight(data_file_light):
        _light_temps = []

        # ファイルの存在を確認
        is_file = os.path.exists(data_file_light)
        if not is_file:
            print("正しいファイル名を指定してください。")
            sys.exit(1)

        # ファイルを開いてデータを取得
        with open(data_file_light) as f:
            _lines = f.readlines()
            for _line in _lines:
                _data = _line.split()
                _light_temps.append(_data[0])

        return _light_temps


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
    cpu_temps = []
    cur_temps = []
    max_temps = []
    light_temps = []


    print(data_file + " のデータをThingSpeakに登録します。")
    print(data_file_capa_cur + " のデータをThingSpeakに登録します。")
    print(data_file_capa_max + " のデータをThingSpeakに登録します。")
    print(data_file_light + " のデータをThingSpeakに登録します。")

    # CPU温度の情報をファイルから取得
    cpu_temps = getCpuTempFromFile(data_file)
    cur_temps = getCurrentCapa(data_file_capa_cur)
    max_temps = getMaxCapa(data_file_capa_max)
    light_temps = getLight(data_file_light)

    print("CPU温度のデータが " + str(len(cpu_temps)) + " 件あります。")
    print("カレントバッテリーのデータが " + str(len(cur_temps)) + " 件あります。")
    print("maxのバッテリーデータが " + str(len(max_temps)) + " 件あります。")
    print("画面の明るさのデータが " + str(len(light_temps)) + " 件あります。")
    
    # データの中身をすべて表示
    # print(cpu_temps)
    # print(cur_temps)
    # print(max_temps)
    # print(light_temps)

    # 最新のデータ（一番最後）をThingSpeakに登録
    # 登録するデータを設定
    post_data = {'field1': cpu_temps[-1]}
    post2ThingSpeak(ts_update_url, headers, post_data)

    post_data = {'field2': cur_temps[-1]}
    post2ThingSpeak(ts_update_url, headers, post_data)

    post_data = {'field3': max_temps[-1]}
    post2ThingSpeak(ts_update_url, headers, post_data)

    post_data = {'field4': light_temps[-1]}
    post2ThingSpeak(ts_update_url, headers, post_data)

    print("CPU温度：" + str(cpu_temps[-1]) + " を登録しました。")
    print("カレントバッテリー：" + str(cur_temps[-1]) + " を登録しました。")
    print("maxバッテリー：" + str(max_temps[-1]) + " を登録しました。")
    print("明るさ：" + str(light_temps[-1]) + " を登録しました。")


    battery = float(max_temps[-1]) * 0.5

    if float(battery) >= float(cur_temps[-1]):
        print("充電が50%未満です")
        # sys.exit(0)

    if float(cpu_temps[-1]) >= 90.0: #とても熱い
        if float(light_temps[-1]) >= 500: #画面が明るい
            if float(battery) >= float(cur_temps[-1]): #バッテリーが50%以下
                send_gmail.gmail5()
            else:
                send_gmail.gmail6()
        else:
            if float(battery) >= float(cur_temps[-1]): #バッテリーが50%以下
                send_gmail.gmail3()
            else:
                send_gmail.gmail1()
        # sys.exit(0)
    elif float(cpu_temps[-1]) >= 70.0: #熱くなってきた
        if float(light_temps[-1]) >= 500: #画面が明るい
            if float(battery) >= float(cur_temps[-1]): #バッテリーが50%以下
                send_gmail.gmail7()
            else:
                send_gmail.gmail8()
        else:
            if float(battery) >= float(cur_temps[-1]): #バッテリーが50%以下
                send_gmail.gmail4()
            else:
                send_gmail.gmail2()
        # sys.exit(0)
    else:
        print("温度は70未満です。")


#1分毎にjobを実行
schedule.every(5).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

# sys.exit(0)