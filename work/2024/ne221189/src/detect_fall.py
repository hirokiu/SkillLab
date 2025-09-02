import os
import sys
import requests # httpリクエストを行うためのモジュール
import re       # 正規表現を使うためのモジュール
import time
import math

data_file = "/home/wadakyosuke/csn_raspi/data/csn.log"

api_key = 'S6GSTL0OXXYOEVJQ'    # 作成したチャンネルのAPIキー
channle_id = '2646847'          # 作成したチャンネルのID

_ts_base_url = "https://api.thingspeak.com"
ts_update_url = _ts_base_url + "/update"

# HTTPでのデータ登録のための設定
headers = {'X-THINGSPEAKAPIKEY': api_key}

def post2ThingSpeak(req_url, headers, post_data):
	while True:
		response = requests.post(req_url, headers=headers, data=post_data)
		if response.text != '0':
			break
		time.sleep(1)

# 引数: string ファイルのパス
# 返り値: float4つ(時間, x軸加速度, y軸加速度, z軸加速度)
def readData(filepath, num_lines=800):
	with open(filepath) as f:
		lines = f.readlines()[-num_lines:]  # 最新の800行を読み込む
	data = []
	for line in lines:
		t,x,y,z = line.strip().split(',')
		data.append((float(t), float(x), float(y), float(z)))
	return data

def calcVec(x,y,z):
	return math.sqrt(x**2 + y**2 + z**2)

def isFallen(pre,cur,threshold=1.0):
	diff = abs(cur - pre)
	return diff > threshold, diff

def recordFall(diff):
	print("This furniture is probably fallen down!")
	post_data = {'field1': diff}
	post2ThingSpeak(ts_update_url,headers,post_data)
	print("衝撃:" + str(diff) + " を登録しました。")

def monitor(filepath):
	interval = 15
	num_lines = 800

	while True:
		data = readData(filepath,num_lines=num_lines)
		pre = None
		flag = False
		max_diff = 0.0

		for t,x,y,z in data:
			cur = calcVec(x,y,z)
			if pre is not None:
				fallen,diff = isFallen(pre,cur)
				if fallen:
					max_diff = max(max_diff,diff)
					flag = True
			pre = cur

		if flag:
			recordFall(max_diff)
		time.sleep(interval)

monitor(data_file)
