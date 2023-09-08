#!/bin/bash

BASE_DIR=/home/pi/csn_raspi
TARGET_DIR=${BASE_DIR}/active

TODAY=`date +'%Y%m%d'`
LASTTIME=`date +'%s'`

# process check
EXEC_CMD=${BASE_DIR}/executeGetData/smsExecute
IS_RUN=`ps -ef | grep ${EXEC_CMD} | grep -v grep | wc -l`
if [ ${IS_RUN} = 0 ]; then
  ${BASE_DIR}/tools/runSMSExecute.sh
fi

START=${TARGET_DIR}/start.txt
ALIVE=${TARGET_DIR}/alive_${TODAY}.txt
if [ -e ${START} ]; then
    echo ${LASTTIME} >> ${ALIVE}
else
    touch ${START}
    touch ${ALIVE}
    echo ${LASTTIME} > ${START}
fi
