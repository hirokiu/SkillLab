#!/bin/bash

while true
do
    # Raspberry PiのCPU温度の取得
    cpu_temp=$(vcgencmd measure_temp | sed "s/temp=\(.*\)'C/\1/")

    # 温度が40度未満の場合、保存
    if [ $(echo "$cpu_temp < 40.0” | bc -l) -eq 1 ]
    then
        echo "$(date +%Y-%m-%dT%H:%M:%S" "%Z), 　　　　○○○○□□□□○○○○□□□□○○○○" >> cpu_temp.dat
    fi
    sleep 3
done    
