#!/bin/bash

while true
do
#    /usr/bin/powermetrics -b 1 -n 1 -s tasks --show-process-energy --show-process-io | sed -l "s/^/$(date +%Y-%m-%dT%H:%M:%S" "%Z) /" >> ./data/process_energy_io.dat
    
    /usr/bin/powermetrics -b 1 -n 1 -s smc | grep "CPU die temperature" | sed -l "s/^/$(date +%Y-%m-%dT%H:%M:%S" "%Z) /" >> ./data/cpu_temp.dat
    ioreg -l | grep CurrentCapacity | tail -n 1 >> ./data/capa_cur.dat
    ioreg -l | grep MaxCapacity | tail -n 1 >> ./data/capa_max.dat
    sudo powermetrics -n 1 | grep "Backlight level" | awk '{print $3}' >> ./data/light.dat

    sleep 10

done
