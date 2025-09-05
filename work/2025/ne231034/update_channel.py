#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import os
import sys
import requests # httpリクエストを行うためのモジュール
import re       # 正規表現を使うためのモジュール

api_key = ''    # 作成したチャンネルのAPIキー
channle_id = ''          # 作成したチャンネルのID
data_file = "cpu_temp.dat"      # Raspberry Piの温度を記録したファイルのパス

_ts_base_url = "https://api.thingspeak.com"
ts_update_url = _ts_base_url + "/update"
# GET https://api.thingspeak.com/update?api_key=MSUJ80Z21B6XIS7G&field1=0

# HTTPでのデータ登録のための設定
headers = {'X-THINGSPEAKAPIKEY': api_key}


#------
# get_cpu_temp.shで取得したCPU tempartureの値を取得して、配列を返す
# 引数：データが入ったファイルのパス
# return : cpu_temp リスト（配列）
# 2023-09-06T12:11:49 JST, temp=44.0'C
#------
def getCpuTempFromFile(filename):

    _cpu_temps = []

    # ファイルを開いてデータを取得
    with open(filename) as f:
        _lines = f.readlines()
        for _line in _lines: # 配列を1行ずつ取り出す
            _data = _line.split() # ファイルの1行を空白で区切って配列にする
            print(_data) # 1行の中身を確認
            # ['2023-09-06T12:11:49', 'JST,', "temp=44.0'C"]
            # ここで、1行のデータのどの部分をどう使うか考えて処理する
            res = re.match(r'temp=([0-9.]*)\'C', _data[2]) # 正規表現を使って温度を取り出し
            if res :
                print(res.group(1)) # マッチしたパターンのうち、()の部分を取り出し
                _cpu_temps.append(res.group(1)) # 取得したパターンを結果用の配列に追記する
    
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
cpu_temps = []


print(data_file + " のデータをThingSpeakに登録します。")
# CPU温度の情報をファイルから取得
cpu_temps = getCpuTempFromFile(data_file)

print("CPU温度のデータが " + str(len(cpu_temps)) + " 件あります。")
# データの中身をすべて表示
print(cpu_temps)

# 最新のデータ（一番最後）をThingSpeakに登録
# 登録するデータを設定
post_data = {'field1': cpu_temps[-1]}
post2ThingSpeak(ts_update_url, headers, post_data)

print("CPU温度：" + str(cpu_temps[-1]) + " を登録しました。")
sys.exit(0)
