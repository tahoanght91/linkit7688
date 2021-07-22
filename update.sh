#!/bin/ash
if [[ ! -z "$1" ]] && [[ ! -z "$2" ]]
then
  /etc/init.d/7688 stop
  cp /IoT/linkit7688/config/devices.json /IoT
  cp /IoT/linkit7688/last_cmd_alarm.json /IoT
  cp /IoT/linkit7688/last_cmd_network.json /IoT
  cp /IoT/linkit7688/last_rfid_card_code.json /IoT
  cp /IoT/linkit7688/lcd_setting_data_file.json /IoT
  if curl -LO $1 --max-time 5
  then
    echo 'Download source code successful'
    mv /IoT/linkit7688 /
    unzip $2
    echo 'Unzip successful'
    mv /IoT/linkit7688-$2 linkit7688
    cp /IoT/devices.json /IoT/linkit7688/config/
    cp /IoT/last_cmd_alarm.json /IoT/linkit7688/
    cp /IoT/last_cmd_network.json /IoT/linkit7688/
    cp /IoT/last_rfid_card_code.json /IoT/linkit7688/
    cp /IoT/lcd_setting_data_file.json /IoT/linkit7688/
    cp /IoT/linkit7688/update.sh /IoT
    echo 'Copy 6 files to linkit7688 successful'
    chmod +x /IoT/update.sh
    rm -rf /linkit7688
    rm -rf /IoT/$2.zip
    echo 'Remove old version linkit7688 and source code (.zip) successful'
    /etc/init.d/7688 start
  else
    echo 'CURL failed'
    /etc/init.d/7688 start
  fi
else
  echo 'Need exactly 2 parameters'
fi