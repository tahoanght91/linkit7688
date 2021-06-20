uci set network.lan.ipaddr='10.6.71.88'
uci set network.lan.gateway='10.6.71.99'
uci set network.lan.netmask='255.255.255.0'
uci set network.lan.proto='static'
uci commit
reboot