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
        last_index = len(reader) - 1
        return reader[last_index]

if __name__ == "__main__":
    _data = getCurrentData()
    print(_data)
