#!/bin/sh

echo "___START___"
BASE_DIR=`pwd`
echo "現在のディレクトリは${BASE_DIR}です"
ls -al


echo "${BASE_DIR}以下のシェルスクリプトのファイルから、echoコマンドを探します。"
FILELIST=`find ${BASE_DIR} -name '*.sh'`
for _FILENAME in ${FILELIST[@]}; do
	echo "ファイル${_FILENAME}内のechoコマンド"
	grep "echo" ${_FILENAME}
done

exit 

