#!/usr/bin/python
# -*- coding: utf-8 -*-

import spidev
import time
from collections import deque
import signal
import sys
from datetime import date
from datetime import datetime

# センサーがつながっているMCP3008のチャネル
temp_channel   = 0
acc_z_channel  = 1

# キューに保存するデータの最大数
max_data = 60

# SPIバスへのアクセスを開く
spi = spidev.SpiDev()
spi.open(0,0)

def ReadChannel(channel):
  """
  MCP3008経由でアナログセンサからのデータを受け取る。
  channelはMCP3008の入力チャンネルで、0から7の値
                r = spi.xfer2([1,(2+channel)<<6,0])      #(*1)を参照  

                ret = ((r[1]&31) << 6) + (r[2] >> 2)    #(*2)　を参照  
  """
  adc = spi.xfer2([1,(2+channel)<<6,0])
  data = ((adc[1]&31) << 6) + (adc[2] >> 2)
  return data

def ConvertVolts(data, places):
  """
  MCP3008から受け取ったデジタルデータを、アナログセンサの
  出力電圧に変換する計算をする。placesは有効桁数。

  """
  volts = (data * 3.3) / float(1023)
  #volts = round(volts, places)
  return volts

def ConvertTemp(volts, places):
  """
  電圧をセンサーが検知した温度に変換する。
  """
  temp = ( 100 * volts ) - 50.0
  temp = round( temp, places )
  return temp

def exit_handler(signal, frame):
  """
  Ctrl+Cが押されたときにデバイスを初期状態に戻して終了する。
  """
  print("\nExit")
  spi.close()
  sys.exit(0)

#
# メインルーチン
#

# 終了時に処理するシグナルハンドラを準備
signal.signal(signal.SIGINT, exit_handler)

# データ保管用のキューを用意
queue = deque()

# ログファイルの用意
# tsvfile = open('data'+datetime.now().strftime("%Y%m%d_%H%M%S")+'.tsv', 'a')
tsvfile = open('data.tsv', 'a')
data_count = 0

while True:

  time.sleep(0.2)

  # 温度センサーを読む
  temp = ConvertTemp( ConvertVolts( ReadChannel( temp_channel ), 4), 4)

  # 加速度センサーを読む
  # TODO:ConvertAcc関数を作成
  acc_z  = ConvertTemp( ConvertVolts( ReadChannel( acc_z_channel ), 4), 4)

  # 平均値を出すためにデータを保存しておく
  # 一定の数データが溜まったら、古い物から削除
  queue.append((temp, acc_z))
  if len(queue) > max_data:
    queue.popleft()

  # 平均値を求める
  sum1 = 0.0
  sum2 = 0.0
  for d in queue:
        sum1 += d[0]
        sum2 += d[1]
  ave_temp = sum1 / len(queue)
  ave_acc_z  = sum2 / len(queue)

  # コンソールへ結果を表示
  print "(温度, 明度)=(%6.2f, %6.2f) 平均 = (%6.2f, %6.2f)" % (temp, acc_z, ave_temp, ave_acc_z)

  # 一定の回数ごとに平均値を記録
  data_count += 1
  if data_count == max_data:
    d = datetime.now()
    tsvfile.write("%s\t%6.2f\t%6.2f\n" % (datetime.now().strftime("\"%Y/%m/%d %H:%M:%S\""), ave_temp, ave_acc_z))
    tsvfile.flush()
    data_count = 0

  time.sleep(0.8)
