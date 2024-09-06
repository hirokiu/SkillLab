#!/bin/bash
# 28 30 * * * * rsync -auz /home/pi/csn_raspi/data balog:/home/pi/kimlab_rsync_dir/`hostname`/
# 30 * * * * /bin/bash /home/pi/csn_raspi/tools/rsync2nas.sh 

HOSTNAME=`hostname`
TARGET_NAS=163.212.95.200
RSYNC_USER=csn_pi
TARGET_HOST=kimlabDisk

BASE_DIR=/home/pi/csn_raspi
DATA_DIR=${BASE_DIR}/data
TRIG_DIR=${BASE_DIR}/earthquakes
TARGET_DIR=/volume1/kimlab-shared/data/${HOSTNAME}

DEFAULT_HOSTNAME="raspberrypi"
echo "if HOSTNAME is default(raspberrypi), will be exit..."
sleep 1
if [ ${HOSTNAME} == ${DEFAULT_HOSTNAME} ]
then
    echo "...HOSTNAME is default(raspberrypi)."
    exit 1
fi

echo "rsync to NAS start..."
sleep 1
# rsync -avh /home/pi/csn_raspi/earthquakes/ csn_pi@192.168.11.8:/volume1/kimlab-shared/data/csn_ycu_01
echo "rsync -auz ${DATA_DIR} ${RSYNC_USER}@${TARGET_NAS}:${TARGET_DIR}/"
#rsync -e 'ssh -i ~/.ssh/csn_pi_rsa' -auz ${DATA_DIR} ${RSYNC_USER}@${TARGET_NAS}:${TARGET_DIR}/
rsync -auz ${DATA_DIR} ${TARGET_HOST}:${TARGET_DIR}/
sleep 1
echo "rsync -auz ${TRIG_DIR} ${RSYNC_USER}@${TARGET_NAS}:${TARGET_DIR}/"
#rsync -e 'ssh -i ~/.ssh/csn_pi_rsa' -auz ${TRIG_DIR} ${RSYNC_USER}@${TARGET_NAS}:${TARGET_DIR}/
rsync -auz ${TRIG_DIR} ${TARGET_HOST}:${TARGET_DIR}/

echo "rsync to NAS DONE."
exit 0