#!/bin/ash
/etc/init.d/7688 stop
cp /IoT/linkit7688/config/devices.json /IoT
cp /IoT/linkit7688/last_cmd_alarm.json /IoT
cp /IoT/linkit7688/last_cmd_network.json /IoT
cp /IoT/linkit7688/last_rfid_card_code.json /IoT
cp /IoT/linkit7688/lcd_setting_data_file.json /IoT
if curl -LO $1 --max-time 5
then
  mv /IoT/linkit7688 /
  unzip huyfr
  mv /IoT/linkit7688-huyfr linkit7688
  cp /IoT/devices.json /IoT/linkit7688/config/
  cp /IoT/last_cmd_alarm.json /IoT/linkit7688/
  cp /IoT/last_cmd_network.json /IoT/linkit7688/
  cp /IoT/last_rfid_card_code.json /IoT/linkit7688/
  cp /IoT/lcd_setting_data_file.json /IoT/linkit7688/
  cp /IoT/linkit7688/update.sh /IoT
  chmod +x /IoT/update.sh
  rm -rf /linkit7688
  rm -rf /IoT/huyfr.zip
  /etc/init.d/7688 start
else
  echo 'CURL failed'
  /etc/init.d/7688 start
fi