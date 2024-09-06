#!/usr/bin/python
# -*- coding: utf-8 -*- 

import sys

base_dir = '/home/shishido_1070'
prj_dir = base_dir + '/csn_raspi'
data_dir = prj_dir + '/data'
base_filename = 'csn.log'

def getCurrentData():
    with open(data_dir + '/' + base_filename, mode='r') as f:
        reader = f.readlines()
        # 文字列を数値に変換
        numeric_data = [float(line.strip()) for line in reader]

        #last_index = len(reader) - 1
        ave = sum(numeric_data) / len(reader)
        #return reader[last_index]
        return ave

if __name__ == "__main__":
    _data = getCurrentData()
    print(_data)
