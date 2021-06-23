/etc/init.d/7688 stop
cp /IoT/linkit7688/config/devices.json /IoT
mv /IoT/linkit7688 /
curl -LO https://github.com/huyfr/linkit7688/archive/refs/heads/huyfr.zip
unzip huyfr
mv /IoT/linkit7688-huyfr linkit7688
cp /IoT/devices.json /IoT/linkit7688/config/
rm -rf /linkit7688
rm -rf /IoT/huyfr.zip
/etc/init.d/7688 start