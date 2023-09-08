#!/bin/bash

#    /usr/bin/powermetrics -b 1 -n 1 -s tasks --show-process-energy --show-process-io | sed -l "s/^/$(date +%Y-%m-%dT%H:%M:%S" "%Z) /" >> ./data/process_energy_io.dat
#    /usr/bin/powermetrics -b 1 -n 1 -s smc | grep "CPU Thermal level" | sed -l "s/^/$(date +%Y-%m-%dT%H:%M:%S" "%Z) /" >> ./data/cpu_thermal.dat

vcgencmd measure_temp | sed "s/^/$(date +%Y-%m-%dT%H:%M:%S" "%Z), /" > current_cpu_temp.dat #そのときそのときの温度を取得するので、その都度上書きする。

python overheat_warning.py
