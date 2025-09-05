#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import requests
import time
import PySimpleGUI as sg

sg.theme('DarkAmber')   # デザインテーマの設定

# ウィンドウに配置するコンポーネント
layout = [ [sg.Button('起動'), sg.Button('停止')] ]

# ウィンドウの生成
window = sg.Window('CPU温度監視プログラム', layout)

# イベントループ
while True:
    
    event, values = window.read()
    
    if event == sg.WIN_CLOSED or event == '停止':
        break
        
    elif event == '起動':
        for i in range(10):
            print("ssssssssss")


window.close()