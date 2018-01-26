route add -net 10.10.10.0 netmask 255.255.255.0 dev eth0
route -n
ping 10.10.10.0 -c 3
