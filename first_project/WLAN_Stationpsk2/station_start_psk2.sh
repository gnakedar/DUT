uci set wireless.@wifi-device[0].disabled=0
uci set wireless.@wifi-iface[0].mode=sta
uci set wireless.@wifi-iface[0].ssid='HTC1'
uci set wireless.@wifi-iface[0].network=wlan
uci set wireless.@wifi-iface[0].encryption=psk2
uci set wireless.@wifi-iface[0].key=1234567890
uci commit wireless
/etc/init.d/network reload
ps -w | grep wpa_supplicant
iwinfo
wpa_cli status
