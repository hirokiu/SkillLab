#!/bin/bash

BASE_DIR=/home/pi/csn_raspi
TARGET_DIR=${BASE_DIR}/ascii_data

# must set same nums START,END
#walk_outside
TIME_START_ARRAY=()
TIME_END_ARRAY=()

DB_NAME=csn
TABLE_NAME=Event

COUNT=0
# START,ENDの間のデータをテキストファイルにリダイレクト
for TIME_ITEM in ${TIME_START_ARRAY[@]}; do
  DUMP_FILE=${TARGET_DIR}/data_${TIME_ITEM}.txt
  mysql -u root ${DB_NAME} -e "SELECT t0active,x_acc,y_acc,z_acc FROM ${TABLE_NAME} WHERE t0active >= ${TIME_ITEM} AND t0active < ${TIME_END_ARRAY[${COUNT}]} ORDER BY t0active" > ${DUMP_FILE}
  COUNT=$(( COUNT + 1 ))
done
