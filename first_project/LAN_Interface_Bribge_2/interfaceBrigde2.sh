uci get network.lan.ipaddr
cat /var/dhcp.leases
ping -c 3
uci set network.lan.ipaddr
/etc/init.d/network reload
uci get network.lan.ipaddr
ping -c 3
reset_all
