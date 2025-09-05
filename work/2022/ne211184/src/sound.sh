#!/bin/sh


read X
read Y
read Z

ALERT="かなり揺れています"

if [ $X -ge 10 ]||[ $X -le -10 ]; then
 echo $ALERT
 afplay /System/Library/Sounds/Submarine.aiff
elif [ $Y -ge 10 ]||[ $Y -le -10 ]; then
 echo $ALERT
 afplay /System/Library/Sounds/Submarine.aiff
elif [ $Z -ge 10 ]||[ $Z -le -10 ]; then
 echo $ALERT
 afplay /System/Library/Sounds/Submarine.aiff
fi
