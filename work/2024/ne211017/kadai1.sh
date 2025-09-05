#!/bin/sh

echo "___START___"
BASE_DIR=`pwd`
echo "現在のディレクトリは${BASE_DIR}です"
du -h -d 1 ./ | sort -k 1 -h
echo "${BASE_DIR}内のディレクトリごとのディスク使用量を表示"

exit
