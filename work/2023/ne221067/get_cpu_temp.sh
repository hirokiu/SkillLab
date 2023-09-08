#!/bin/bash

while true
do
#    /usr/bin/powermetrics -b 1 -n 1 -s tasks --show-process-energy --show-process-io | sed -l "s/^/$(date +%Y-%m-%dT%H:%M:%S" "%Z) /" >> ./data/process_energy_io.dat
#   /usr/bin/powermetrics -b 1 -n 1 -s smc | grep "CPU Thermal level" | sed -l "s/^/$(date +%Y-%m-%dT%H:%M:%S" "%Z) /" >> ./data/cpu_thermal.dat

# Raspberry PiのCPU温度を取得保存,sedのところは日時の取得で使用されてる
vcgencmd measure_temp | sed "s/^/$(date +%Y-%m-%dT%H:%M:%S" "%Z), /" >> cpu_temp.dat

    sleep 3
done
