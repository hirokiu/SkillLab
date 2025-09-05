#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import requests # httpリクエストを行うためのモジュール
import re       # 正規表現を使うためのモジュール
import time 

api_key = 'CAENQA2F06AN0E53'    # 作成したチャンネルのAPIキー
channle_id = '2647494'          # 作成したチャンネルのID

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

base_dir = '/home/shishido_1070'
prj_dir = base_dir + '/csn_raspi'
data_dir = prj_dir + '/data'
base_filename = 'csn.log'

def getMaxData():
    with open(data_dir + '/' + base_filename, mode='r') as f:
        reader = f.readlines()
        if len(reader) >= 3000 : #配列の要素が3000行以上なら
            last_lines = reader[-3000:]#後ろから3000行を対象とする
        else: #配列の要素が3000行未満なら
            last_lines = reader#要素全てを対象とする

        x_values = []#x軸の加速度
        y_values = []#x軸の加速度
        z_values = []#x軸の加速度

        for line in last_lines:#整数型から数値型へ
            split_values = line.split(',')
            x_values.append(float(split_values[1]))
            y_values.append(float(split_values[2]))
            z_values.append(float(split_values[3]))
        
        # 各軸の絶対値が最大の値を取得
        max_x = max(x_values, key=abs)
        max_y = max(y_values, key=abs)
        max_z = max(z_values, key=abs)

        # 各軸の最大値リスト
        xyz_max = [max_x, max_y, max_z]

        max_value = max(xyz_max, key=abs)#x、y、zを比較して最も絶対値大きい値を格納
        xyz_max_idx = xyz_max.index(max_value)#最も絶対値が大きい値は何軸かを格納
        
        target_idx = None
        if xyz_max_idx == 0:#x軸の加速度が最も大きい値の場合
            target_idx = x_values.index(max_value)

        elif xyz_max_idx == 1:#y軸の加速度が最も大きい値の場合
            target_idx = y_values.index(max_value)

        elif xyz_max_idx == 2:#z軸の加速度が最も大きい値の場合
            target_idx = z_values.index(max_value)

        target_value = last_lines[target_idx].split(',')#最も大きい値があった要素を格納
        float_target_value = [float(i) for i in target_value]#整数型から数値型へ変換
        return float_target_value

# if __name__ == "__main__":
#     _data = getCurrentData()
#     print(_data)


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
turning_over = []


print(base_filename + " のデータをThingSpeakに登録します。")
# 加速度の情報をファイルから取得
turning_over = getMaxData()

# データの中身をすべて表示
print(turning_over)

# 最大のデータをThingSpeakに登録
# 登録するデータを設定
post_data_x = {'field1': turning_over[1]}
post_data_y = {'field2': turning_over[2]}
post_data_z = {'field3': turning_over[3]}
post2ThingSpeak(ts_update_url, headers, post_data_x)
post2ThingSpeak(ts_update_url, headers, post_data_y)
post2ThingSpeak(ts_update_url, headers, post_data_z)


print("加速度：" + str(turning_over) + " を登録しました。")
sys.exit(0)
