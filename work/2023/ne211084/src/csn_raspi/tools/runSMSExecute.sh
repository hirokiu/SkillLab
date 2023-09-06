#!/bin/bash

BASE_DIR=/home/pi/csn_raspi/executeGetData
# process check
EXEC_CMD=${BASE_DIR}/smsExecute
#LOG_DIR=${BASE_DIR}/logs
LOG_DIR=/tmp
IS_RUN=`ps -ef | grep ${EXEC_CMD} | grep -v grep | wc -l`
if [ ${IS_RUN} = 0 ]; then
  nohup ${EXEC_CMD} 2> ${LOG_DIR}/err.log < /dev/null &
  #nohup ${EXEC_CMD} > ${LOG_DIR}/out.log 2> ${LOG_DIR}/err.log < /dev/null &
  #${EXEC_CMD} > ${LOG_DIR}/out.log 2> ${LOG_DIR}/err.log < /dev/null &
fi
