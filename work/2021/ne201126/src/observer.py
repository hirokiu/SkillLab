#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter import messagebox

import os
import sys
import requests
import time
import PySimpleGUI as sg
import subprocess

sg.theme('DarkAmber')   # デザインテーマの設定

# ウィンドウに配置するコンポーネント
layout = sg.Button('監視を起動'), sg.Button('停止')

# ウィンドウの生成
window2 = sg.Window('CPU温度監視プログラムサブ', layout)

# イベントループ
while True:
    event, values = window2.read()
    if event == sg.WIN_CLOSED or event == '停止':
        break
    elif event == '監視を起動':
        print(subprocess.run("sudo ./get_cpu_temp.sh", shell=True))  
        

window2.close()