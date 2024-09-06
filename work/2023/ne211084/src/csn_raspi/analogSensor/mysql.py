!/usr/bin/python
# -*- coding: utf-8 -*-

import spidev
import time
from collections import deque
import signal
import sys
from datetime import date
from datetime import datetime

import MySQLdb
from MySQLdb.cursors import DictCursor

# センサーがつながっているMCP3002のチャネル
# 温度センサーのみ
temp_channel   = 0

# SPIバスへのアクセスを開く
spi = spidev.SpiDev()
spi.open(0,0)

#============================
# 関数　
#============================
def ReadChannel(channel):
  """
  MCP3002経由でアナログセンサからのデータを受け取る。
  """
  adc = spi.xfer2([1,(2+channel)<<6,0])
  data = ((adc[1]&31) << 6) + (adc[2] >> 2)
  return data

def ConvertVolts(data, places):
  """
  MCP3002から受け取ったデジタルデータを、アナログセンサの
  出力電圧に変換する計算をする。placesは有効桁数。
  """
  volts = (data * 3.3) / float(1023)
  volts = round(volts, places)
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
  # MySQLの切断
  cursor.close()
  connection.close()
  # SPIデバイスの切断　
  spi.close()
  sys.exit(0)

#============================
# メイン処理
#============================
# 終了時に処理するシグナルハンドラを準備
signal.signal(signal.SIGINT, exit_handler)

# MySQL接続
connection = MySQLdb.connect(db="c4y3",user="root")
cursor = connection.cursor()

# 温度の表示処理を無限ループ
while True:

  # 取得するインターバル　
  time.sleep(0.2)

  # 温度センサーを読む
  temp = ConvertTemp( ConvertVolts( ReadChannel( temp_channel ), 4), 4)

  # 現在時刻を取得
  timeStr = datetime.now().strftime( '%Y-%m-%d %H:%M:%S' )

  # データベースへ保存
  sql = "INSERT INTO temperture (temp,datetime) VALUES ('" + str(temp) + "','" + timeStr + "')"

  # コンソールへ結果を表示
  print "%6.2f度" % temp

  time.sleep(0.8)
