#!/bin/sh

echo '___START___'
cd /home/shishido_1070/Desktop
BASE_DIR=`pwd`
ls -al
echo "${BASE_DIR}内のファイルリストを表示しました。"
echo ""
echo "${BASE_DIR}内のファイルリストをサイズの降順に並べ替えます。"
ls -alh | sort -k 5 -h -r
exit
