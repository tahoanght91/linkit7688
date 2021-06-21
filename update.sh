/etc/init.d/7688 stop
cp /IoT/linkit7688/config/devices.json /IoT
rm -rf linkit7688
git clone https://github.com/huyfr/linkit7688.git
cd linkit7688
git checkout huyfr
cp /IoT/devices.json /IoT/linkit7688/config/
/etc/init.d/7688 start