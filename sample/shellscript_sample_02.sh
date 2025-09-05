#!/bin/sh

echo ”___START___”
BASE_DIR=`pwd`
echo “現在のディレクトリは${BASE_DIR}です”
ls -al
echo “${BASE_DIR}内のファイルリストを表示しました。”
echo ""
echo “${BASE_DIR}内のファイルリストをサイズの降順に並べ替えます。”
ls -alh | sort -k 5 -h -r


echo “${BASE_DIR}以下のファイル名をすべて取得します。”
FILELIST=`find ${BASE_DIR} -name '*.*'`
for _FILES in ${FILELIST[@]}; do
    echo ${_FILES}
    FILENAME=${_FILES##*/}
    echo "${FILENAME}と同じ名前のをファイル探します。"
    find ${HOME}/Documents -name '${FILENAME'
done

exit 

