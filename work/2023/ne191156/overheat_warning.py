#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import requests
import re
import time #これをしないとtime.sleepは機能しません。
api_key = 'IBLURH03FBZGCP3F'
channle_id = '2262907'
data_file = "current_cpu_temp.dat"

_ts_base_url = "https://api.thingspeak.com"
ts_update_url = _ts_base_url + "/update"
# GET https://api.thingspeak.com/update?api_key=MSUJ80Z21B6XIS7G&field1=0

# HTTPでのデータ登録のための設定
headers = {'X-THINGSPEAKAPIKEY': api_key}


#------
# CPU die tempartureの値を取得して、配列を返す
# 引数：データが入ったファイルのパス
# return : cpu_temp 
# 2021-09-07T23:59:36 JST CPU die temperature: 69.77 C
#------
def getCpuTempFromFile(filename):

    _cpu_temp = 0.0

    # ファイルの存在を確認
    is_file = os.path.exists(filename)
    if not is_file:
        print(filename + "が存在しないようです。〇〇までお問い合わせください。")
        sys.exit(1)

    # ファイルを開いてデータを取得
    with open(filename) as f:
        _lines = f.readlines() #といっても１行しかないけど
        for _line in _lines: # 配列を1行ずつ取り出す
            _data = _line.split() # ファイルの1行を空白で区切って配列にする
            #print(_data) # 1行の中身を確認（以下、デバッグのためのprintはコメントアウト）
            # ここで、1行のデータのどの部分をどう使うか考えて処理する
            res = re.match(r'temp=([0-9.]*)\'C', _data[2])
            if res:
                #print(res.group(1))
                _cpu_temp = res.group(1) # 結果を記録する
    
    return _cpu_temp

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
cpu_temp = 0.0

#print(data_file + " のデータ：")
# CPU温度の情報をファイルから取得
cpu_temp = getCpuTempFromFile(data_file)

#print("CPU温度は " + cpu_temp + " です。")
# データの中身を表示
print(cpu_temp)

# データをThingSpeakに登録（ここでは44.5以上の場合としているが、実際はもっと高い値とする想定）
# 登録するデータを設定
post_data = {'field1': cpu_temp}
if float(cpu_temp) > 44.5:
    post2ThingSpeak(ts_update_url, headers, post_data)

    print("CPU温度が44.5を超えました。作業環境が暑すぎませんか？")
sys.exit(0)
