#!/bin/bash

while true
do
#    /usr/bin/powermetrics -b 1 -n 1 -s tasks --show-process-energy --show-process-io | sed -l "s/^/$(date +%Y-%m-%dT%H:%M:%S" "%Z) /" >> ./data/process_energy_io.dat
    #/usr/bin/powermetrics -b 1 -n 1 -s smc
    power 
    | grep "CPU Thermal level" 
    | sed -l "s/^/$(date +%Y-%m-%dT%H:%M:%S" "%Z) /" 
    >> ./data/cpu_thermal.dat
    sleep 10
done
