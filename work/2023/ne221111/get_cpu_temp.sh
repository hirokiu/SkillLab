#!/bin/bash

while true
do
    # Raspberry PiのCPU温度の取得
    cpu_temp=$(vcgencmd measure_temp | sed "s/temp=\(.*\)'C/\1/")

    # 温度が40度未満の場合、保存
    if [ $(echo "$cpu_temp < 40.0" | bc -l) -eq 1 ]
    then
        echo "$(date +%Y-%m-%dT%H:%M:%S" "%Z), 　　 　-○○○○□□□□○○○○□□□□○○○○, $cpu_temp°C,Low" >> cpu_temp2.dat
    fi

    # 温度が40度以上の場合、保存
    if [ $(echo "$cpu_temp >= 40.0" | bc -l) -eq 1 ] && [ $(echo "$cpu_temp < 40.5" | bc -l) -eq 1 ]
    then
        echo "$(date +%Y-%m-%dT%H:%M:%S" "%Z), 　　　　○○○○□□□□○○○○□□□□○○○○, $cpu_temp°C" >> cpu_temp2.dat
    fi

    if [ $(echo "$cpu_temp >= 40.5" | bc -l) -eq 1 ] && [ $(echo "$cpu_temp < 41.0" | bc -l) -eq 1 ]
    then
        echo "$(date +%Y-%m-%dT%H:%M:%S" "%Z), 　　　　●○○○□□□□○○○○□□□□○○○○, $cpu_temp°C" >> cpu_temp2.dat
    fi

    if [ $(echo "$cpu_temp >= 41.0" | bc -l) -eq 1 ] && [ $(echo "$cpu_temp < 41.5" | bc -l) -eq 1 ]
    then
        echo "$(date +%Y-%m-%dT%H:%M:%S" "%Z), 　　　　●●○○□□□□○○○○□□□□○○○○, $cpu_temp°C" >> cpu_temp2.dat
    fi

    if [ $(echo "$cpu_temp >= 41.5" | bc -l) -eq 1 ] && [ $(echo "$cpu_temp < 42.0" | bc -l) -eq 1 ]
    then
        echo "$(date +%Y-%m-%dT%H:%M:%S" "%Z), 　　　　●●●○□□□□○○○○□□□□○○○○, $cpu_temp°C" >> cpu_temp2.dat
    fi

    if [ $(echo "$cpu_temp >= 42.0" | bc -l) -eq 1 ] && [ $(echo "$cpu_temp < 42.5" | bc -l) -eq 1 ]
    then
        echo "$(date +%Y-%m-%dT%H:%M:%S" "%Z), 　　　　●●●●□□□□○○○○□□□□○○○○, $cpu_temp°C" >> cpu_temp2.dat
    fi

    if [ $(echo "$cpu_temp >= 42.5" | bc -l) -eq 1 ] && [ $(echo "$cpu_temp < 43.0" | bc -l) -eq 1 ]
    then
        echo "$(date +%Y-%m-%dT%H:%M:%S" "%Z), 　　　　●●●●■□□□○○○○□□□□○○○○, $cpu_temp°C" >> cpu_temp2.dat
    fi

    if [ $(echo "$cpu_temp >= 43.0" | bc -l) -eq 1 ] && [ $(echo "$cpu_temp < 43.5" | bc -l) -eq 1 ]
    then
        echo "$(date +%Y-%m-%dT%H:%M:%S" "%Z), 　　　　●●●●■■□□○○○○□□□□○○○○, $cpu_temp°C" >> cpu_temp2.dat
    fi

    if [ $(echo "$cpu_temp >= 43.5" | bc -l) -eq 1 ] && [ $(echo "$cpu_temp < 44.0" | bc -l) -eq 1 ]
    then
        echo "$(date +%Y-%m-%dT%H:%M:%S" "%Z), 　　　　●●●●■■■□○○○○□□□□○○○○, $cpu_temp°C" >> cpu_temp2.dat
    fi

    if [ $(echo "$cpu_temp >= 44.0" | bc -l) -eq 1 ] && [ $(echo "$cpu_temp < 44.5" | bc -l) -eq 1 ]
    then
        echo "$(date +%Y-%m-%dT%H:%M:%S" "%Z), 　　　　●●●●■■■■○○○○□□□□○○○○, $cpu_temp°C" >> cpu_temp2.dat
    fi

    if [ $(echo "$cpu_temp >= 44.5" | bc -l) -eq 1 ] && [ $(echo "$cpu_temp < 45.0" | bc -l) -eq 1 ]
    then
        echo "$(date +%Y-%m-%dT%H:%M:%S" "%Z), 　　　　●●●●■■■■●○○○□□□□○○○○, $cpu_temp°C" >> cpu_temp2.dat
    fi

    if [ $(echo "$cpu_temp >= 45.0" | bc -l) -eq 1 ] && [ $(echo "$cpu_temp < 45.5" | bc -l) -eq 1 ]
    then
        echo "$(date +%Y-%m-%dT%H:%M:%S" "%Z), 　　　　●●●●■■■■●●○○□□□□○○○○, $cpu_temp°C" >> cpu_temp2.dat
    fi

    if [ $(echo "$cpu_temp >= 45.5" | bc -l) -eq 1 ] && [ $(echo "$cpu_temp < 46.0" | bc -l) -eq 1 ]
    then
        echo "$(date +%Y-%m-%dT%H:%M:%S" "%Z), 　　　　●●●●■■■■●●●○□□□□○○○○, $cpu_temp°C" >> cpu_temp2.dat
    fi

    if [ $(echo "$cpu_temp >= 46.0" | bc -l) -eq 1 ] && [ $(echo "$cpu_temp < 46.5" | bc -l) -eq 1 ]
    then
        echo "$(date +%Y-%m-%dT%H:%M:%S" "%Z), 　　　　●●●●■■■■●●●●□□□□○○○○, $cpu_temp°C" >> cpu_temp2.dat
    fi

    if [ $(echo "$cpu_temp >= 46.5" | bc -l) -eq 1 ] && [ $(echo "$cpu_temp < 47.0" | bc -l) -eq 1 ]
    then
        echo "$(date +%Y-%m-%dT%H:%M:%S" "%Z), 　　　　●●●●■■■■●●●●■□□□○○○○, $cpu_temp°C" >> cpu_temp2.dat
    fi

    if [ $(echo "$cpu_temp >= 47.0" | bc -l) -eq 1 ] && [ $(echo "$cpu_temp < 47.5" | bc -l) -eq 1 ]
    then
        echo "$(date +%Y-%m-%dT%H:%M:%S" "%Z), 　　　　●●●●■■■■●●●●■■□□○○○○, $cpu_temp°C" >> cpu_temp2.dat
    fi

    if [ $(echo "$cpu_temp >= 47.5" | bc -l) -eq 1 ] && [ $(echo "$cpu_temp < 48.0" | bc -l) -eq 1 ]
    then
        echo "$(date +%Y-%m-%dT%H:%M:%S" "%Z), 　　　　●●●●■■■■●●●●■■■□○○○○, $cpu_temp°C" >> cpu_temp2.dat
    fi

    if [ $(echo "$cpu_temp >= 48.0" | bc -l) -eq 1 ] && [ $(echo "$cpu_temp < 48.5" | bc -l) -eq 1 ]
    then
        echo "$(date +%Y-%m-%dT%H:%M:%S" "%Z), 　　　　●●●●■■■■●●●●■■■■○○○○, $cpu_temp°C" >> cpu_temp2.dat
    fi

    if [ $(echo "$cpu_temp >= 48.5" | bc -l) -eq 1 ] && [ $(echo "$cpu_temp < 49.0" | bc -l) -eq 1 ]
    then
        echo "$(date +%Y-%m-%dT%H:%M:%S" "%Z), 　　　　●●●●■■■■●●●●■■■■●○○○, $cpu_temp°C" >> cpu_temp2.dat
    fi

    if [ $(echo "$cpu_temp >= 49.0" | bc -l) -eq 1 ] && [ $(echo "$cpu_temp < 49.5" | bc -l) -eq 1 ]
    then
        echo "$(date +%Y-%m-%dT%H:%M:%S" "%Z), 　　　　●●●●■■■■●●●●■■■■●●○○, $cpu_temp°C" >> cpu_temp2.dat
    fi

    if [ $(echo "$cpu_temp >= 49.5" | bc -l) -eq 1 ] && [ $(echo "$cpu_temp < 50.0" | bc -l) -eq 1 ]
    then
        echo "$(date +%Y-%m-%dT%H:%M:%S" "%Z), 　　　　●●●●■■■■●●●●■■■■●●●○, $cpu_temp°C" >> cpu_temp2.dat
    fi


    if [ $(echo "$cpu_temp >= 50" | bc -l) -eq 1 ] && [ $(echo "$cpu_temp < 51" | bc -l) -eq 1 ]
    then
        echo "$(date +%Y-%m-%dT%H:%M:%S" "%Z), 　　　　●●●●■■■■●●●●■■■■●●●●, $cpu_temp°C" >> cpu_temp2.dat
    fi

    if [ $(echo "$cpu_temp >= 51" | bc -l) -eq 1 ] && [ $(echo "$cpu_temp < 52" | bc -l) -eq 1 ]
    then
        echo "$(date +%Y-%m-%dT%H:%M:%S" "%Z), 　　　　●●●●■■■■●●●●■■■■●●●●+, $cpu_temp°C" >> cpu_temp2.dat
    fi
    if [ $(echo "$cpu_temp >= 52" | bc -l) -eq 1 ] && [ $(echo "$cpu_temp < 53" | bc -l) -eq 1 ]
    then
        echo "$(date +%Y-%m-%dT%H:%M:%S" "%Z), 　　　　●●●●■■■■●●●●■■■■●●●●++, $cpu_temp°C" >> cpu_temp2.dat
    fi

    if [ $(echo "$cpu_temp >= 53" | bc -l) -eq 1 ] && [ $(echo "$cpu_temp < 54" | bc -l) -eq 1 ]
    then
        echo "$(date +%Y-%m-%dT%H:%M:%S" "%Z), 　　　　●●●●■■■■●●●●■■■■●●●●+++, $cpu_temp°C" >> cpu_temp2.dat
    fi
    if [ $(echo "$cpu_temp >= 54" | bc -l) -eq 1 ] && [ $(echo "$cpu_temp < 55" | bc -l) -eq 1 ]
    then
        echo "$(date +%Y-%m-%dT%H:%M:%S" "%Z), 　　　　●●●●■■■■●●●●■■■■●●●●++++, $cpu_temp°C" >> cpu_temp2.dat   
    fi
    if [ $(echo "$cpu_temp >= 55" | bc -l) -eq 1 ] && [ $(echo "$cpu_temp < 56" | bc -l) -eq 1 ]
    then
        echo "$(date +%Y-%m-%dT%H:%M:%S" "%Z), 　　　　●●●●■■■■●●●●■■■■●●●●+++++, $cpu_temp°C" >> cpu_temp2.dat
    fi

    if [ $(echo "$cpu_temp >= 56" | bc -l) -eq 1 ] && [ $(echo "$cpu_temp < 57" | bc -l) -eq 1 ]
    then
        echo "$(date +%Y-%m-%dT%H:%M:%S" "%Z), 　　　　●●●●■■■■●●●●■■■■●●●●++++++, $cpu_temp°C" >> cpu_temp2.dat
    fi

    if [ $(echo "$cpu_temp >= 57" | bc -l) -eq 1 ] && [ $(echo "$cpu_temp < 58" | bc -l) -eq 1 ]
    then
        echo "$(date +%Y-%m-%dT%H:%M:%S" "%Z), 　　　　●●●●■■■■●●●●■■■■●●●●+++++++, $cpu_temp°C" >> cpu_temp2.dat
    fi



    if [ $(echo "$cpu_temp >= 58" | bc -l) -eq 1 ] && [ $(echo "$cpu_temp < 59" | bc -l) -eq 1 ]
    then
        echo "$(date +%Y-%m-%dT%H:%M:%S" "%Z), 　　　　●●●●■■■■●●●●■■■■●●●●++++++++, $cpu_temp°C" >> cpu_temp2.dat
    fi


    if [ $(echo "$cpu_temp >= 59" | bc -l) -eq 1 ] && [ $(echo "$cpu_temp < 60" | bc -l) -eq 1 ]
    then
        echo "$(date +%Y-%m-%dT%H:%M:%S" "%Z), 　　　　●●●●■■■■●●●●■■■■●●●●+++++++++, $cpu_temp°C" >> cpu_temp2.dat
    fi


    if [ $(echo "$cpu_temp >= 60" | bc -l) -eq 1 ] && [ $(echo "$cpu_temp < 62" | bc -l) -eq 1 ]
    then
        echo "$(date +%Y-%m-%dT%H:%M:%S" "%Z), 　　　　●●●●■■■■●●●●■■■■●●●●++++++++++, $cpu_temp°C,HIGH" >> cpu_temp2.dat
    fi

    if [ $(echo "$cpu_temp >= 62" | bc -l) -eq 1 ] && [ $(echo "$cpu_temp < 64" | bc -l) -eq 1 ]
    then
        echo "$(date +%Y-%m-%dT%H:%M:%S" "%Z), 　　　　●●●●■■■■●●●●■■■■●●●●++++++++++@, $cpu_temp°C,HIGH" >> cpu_temp2.dat
    fi

    if [ $(echo "$cpu_temp >= 64" | bc -l) -eq 1 ] && [ $(echo "$cpu_temp < 66" | bc -l) -eq 1 ]
    then
        echo "$(date +%Y-%m-%dT%H:%M:%S" "%Z), 　　　　●●●●■■■■●●●●■■■■●●●●++++++++++@@, $cpu_temp°C,HIGH" >> cpu_temp2.dat
    fi

    if [ $(echo "$cpu_temp >= 66" | bc -l) -eq 1 ] && [ $(echo "$cpu_temp < 68" | bc -l) -eq 1 ]
    then
        echo "$(date +%Y-%m-%dT%H:%M:%S" "%Z), 　　　　●●●●■■■■●●●●■■■■●●●●++++++++++@@@, $cpu_temp°C,HIGH" >> cpu_temp2.dat
    fi

    if [ $(echo "$cpu_temp >= 68" | bc -l) -eq 1 ] && [ $(echo "$cpu_temp < 70" | bc -l) -eq 1 ]
    then
        echo "$(date +%Y-%m-%dT%H:%M:%S" "%Z), 　　　　●●●●■■■■●●●●■■■■●●●●++++++++++@@@@, $cpu_temp°C,HIGH" >> cpu_temp2.dat
    fi

    if [ $(echo "$cpu_temp >= 70" | bc -l) -eq 1 ] && [ $(echo "$cpu_temp < 75" | bc -l) -eq 1 ]
    then
        echo "$(date +%Y-%m-%dT%H:%M:%S" "%Z), 　　　　●●●●■■■■●●●●■■■■●●●●++++++++++@@@@@, $cpu_temp°C,VERYHIGH" >> cpu_temp2.dat
    fi

    if [ $(echo "$cpu_temp >= 75" | bc -l) -eq 1 ] && [ $(echo "$cpu_temp < 80" | bc -l) -eq 1 ]
    then
        echo "$(date +%Y-%m-%dT%H:%M:%S" "%Z), 　　　　●●●●■■■■●●●●■■■■●●●●++++++++++@@@@@!, $cpu_temp°C,!VERYHIGH!" >> cpu_temp2.dat
    fi

    if [ $(echo "$cpu_temp >= 80" | bc -l) -eq 1 ]
    then
        echo "$(date +%Y-%m-%dT%H:%M:%S" "%Z), 　　　　●●●●■■■■●●●●■■■■●●●●++++++++++@@@@@!, $cpu_temp°C,!!!ERRORHIGH!!!" >> cpu_temp2.dat
    fi







 
     sleep 3
done
