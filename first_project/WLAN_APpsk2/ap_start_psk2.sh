uci set wireless.@wifi-device[0].disabled=0
uci set wireless.@wifi-iface[0].mode=ap
uci set wireless.@wifi-iface[0].ssid='Rpi3AP-PSK2'
uci set wireless.@wifi-iface[0].network=lan
uci set wireless.@wifi-iface[0].encryption=psk2
uci set wireless.@wifi-iface[0].key=1234567890
uci commit wireless
/etc/init.d/network reload
ps -w | grep hostapd
uci get wireless.@wifi-iface[-1].ssid
hostapd_cli status
iwinfo wlan0 assoclist
iwinfo
