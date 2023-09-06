#!/bin/bash

#============================
# sample data
#  (1349355,5,1424656020.883873,1424656020.885738,-0.059694,0.091967,-9.552595,4,0)
#
# CREATE TABLE `Event` (
#  `id` int(20) NOT NULL AUTO_INCREMENT,
#  `device_id` int(11) NOT NULL,
#  `t0check` double NOT NULL,
#  `t0active` double NOT NULL,
#  `x_acc` double NOT NULL,
#  `y_acc` double NOT NULL,
#  `z_acc` double NOT NULL,
#  `sample_size` int(11) NOT NULL,
#  `offset` int(11) NOT NULL,
#  PRIMARY KEY (`id`)
#) ENGINE=MyISAM AUTO_INCREMENT=1403429 DEFAULT CHARSET=utf8;
#============================

# ディレクトリ設定
BASE_DIR=/home/hiroki_u/mkAscii
FROM_DIR=${BASE_DIR}/data
TARGET_DIR=${BASE_DIR}/ascii

# MySQL設定
DB_NAME=csn
DB_USER=root
TABLE_NAME=Event

# 実行時に指定された引数の数、つまり変数 $# の値が 3 でなければエラー終了。
if [ $# -ne 4 ]; then
  echo "usage sh bz2aschii.sh 'YYYYMMDD' 'HH' 'YYYYMMDD' 'HH'" 1>&2
  exit 1
fi

# 引数で指定された開始時刻を取得
DATETIME_START=${1}${2}
DATETIME_END=${3}${4}
DATETIME_CUR=${DATETIME_START}
DATETIME_START_LINUX=`echo ${1} ${2}`
COUNT=0

while [[ ${DATETIME_CUR} -ne ${DATETIME_END} ]]; do
  BZ2_FILE=${FROM_DIR}/data_${DATETIME_CUR}.sql.bz2
  SQL_FILE=${FROM_DIR}/data_${DATETIME_CUR}.sql
  ASCII_FILE=${TARGET_DIR}/data_${DATETIME_CUR}.csv

  # ファイルの解凍
  bunzip2 ${BZ2_FILE}

  grep "INSERT.*Event[^(]*" ${SQL_FILE} |
    sed -e "s/INSERT INTO \`Event\` VALUES //g" |
    sed -e "s/([0-9.]*,\([0-9.]*\),\([0-9.]*\),\([0-9.]*\),\([0-9.-]*\),\([0-9.-]*\),\([0-9.-]*\),[0-9.]*,[0-9.]*)[,;]/\2,\4,\5,\6\n/g" |
    sort -n |
    sed -e "s/\\n/\
/g" | sed '/^ *$/d' > ${ASCII_FILE}
  # Mac OS X
  # grep "INSERT" ${SQL_FILE} | sed -e "s/([0-9.]*,\([0-9.]*\),[0-9.]*,\([0-9.]*\),\([0-9.-]*\),\([0-9.-]*\),\([0-9.-]*\),[0-9.]*,[0-9.]*)/\2,\3,\4,\5\n/g" > ${ASCII_FILE}

  # データをMySQLにINSERT
  #mysql -u ${DB_USER} < ${SQL_FILE}

  # データをASCIIで書き出し
  #mysql -u ${DB_USER} ${DB_NAME} -e "SELECT t0active,x_acc,y_acc,z_acc FROM ${TABLE_NAME} ORDER BY t0active" > ${ASCII_FILE}

  # NEXT SET
  COUNT=$(( COUNT + 1 ))
  # Raspberry Piの場合
  DATETIME_CUR=`date --date "${DATETIME_START_LINUX} ${COUNT} hours" +%Y%m%d%H`
  # Mac OS X の場合
  #DATETIME_CUR=` date -j -v+${COUNT}H -f %Y%m%d%H ${DATETIME_START} +%Y%m%d%H`

done
