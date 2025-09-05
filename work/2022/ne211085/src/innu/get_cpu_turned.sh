#!/bin/bash

while true
do

#1分に1回、データを送った時の時刻と最終sleepのon時刻が記録される
/usr/bin/pmset -g log | grep "Display is turned on" | tail -n 1 | sed 's/[ ][ ]*/ /g' | sed -l "s/^/$(date +%Y-%m-%dT%H:%M:%S" "%Z) /" >> ./data/cpu_turned.txt

sleep 57 #1分に1回

done
