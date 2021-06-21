/etc/init.d/7688 stop
cp config/devices.json /IoT
rm -rf linkit7688
git clone https://github.com/huyfr/linkit7688.git
cd linkit7688
git checkout huyfr
cd ..
cp devices.json /linkit7688/config
/etc/init.d/7688 start