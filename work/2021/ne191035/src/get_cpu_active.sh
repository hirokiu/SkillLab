#!/bin/bash

while true
do
#    /usr/bin/powermetrics -b 1 -n 1 -s tasks --show-process-energy --show-process-io | sed -l "s/^/$(date +%Y-%m-%dT%H:%M:%S" "%Z) /" >> ./data/process_energy_io.dat
    cpu_active=`/usr/bin/powermetrics -b 1 -n 1 | grep "Avg Num of Cores Active"`
    cpu_active=${cpu_active:25:29}
    cpu_active_o=${cpu_active:0:1}
    if [ $cpu_active_o  -lt 1 ]; then
      echo 現在のCPU使用率は$cpu_active
    fi
    if [ $cpu_active_o -ge 1 ]; then
      echo 現在のCPU使用率は$cpu_active
      echo CPU使用率が１００％を超えています
    fi
    sleep 10

done
