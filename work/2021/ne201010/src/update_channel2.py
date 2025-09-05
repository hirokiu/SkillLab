#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import requests

api_key = 'YBCV0DYM9EGBHTP6'
channle_id = '1500037'
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
cpu_temps = []

#print(data_file + " のデータをThingSpeakに登録します。")
# CPU温度の情報をファイルから取得
cpu_temps = getCpuTempFromFile(data_file)

#print("CPU温度のデータが " + str(len(cpu_temps)) + " 件あります。")
# データの中身をすべて表示

print("現在のCPU温度="+cpu_temps[-1])

if (float(cpu_temps[-1])) > float(80) :
    print('80度をまだ超えています')
else:
    print('80度を超えていません')

#メールを送る文章


import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate


sendAddress = 'youwillbetrush@gmail.com'
password = 'aarvvxggixzhwaal'


subject = 'パソコンからの警告メッセージ'
bodyText = 'パソコンの温度が８０度を超えています。少し使用を控えましょう'
fromAddress = 'youwillbetrush@gmail.com'
toAddress = 'youwillbetrush@gmail.com'

# SMTPサーバに接続
smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
smtpobj.starttls()
smtpobj.login(sendAddress, password)

# メール作成
msg = MIMEText(bodyText)
msg['Subject'] = subject
msg['From'] = fromAddress
msg['To'] = toAddress
msg['Date'] = formatdate()

# 作成したメールを送信
smtpobj.send_message(msg)
smtpobj.close()


#最新のデータのみを出力[-1]とかっこの中に書くことで配列の一番最後のデータのみを出力することができる。

# 最新のデータ（一番最後）をThingSpeakに登録
# 登録するデータを設定
post_data = {'field1': cpu_temps[-1]}
#post2ThingSpeak(ts_update_url, headers, post_data)

print("CPU温度：" + str(cpu_temps[-1]) + " を登録しました。")
sys.exit(0)
