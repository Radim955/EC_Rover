#! /bin/sh
# Changes wifi to wifi name from argument

if [ "$#" != "2" ]; then
       echo "./connectWifi.sh SSID PASSWORD";
       exit 1
fi       

ifconfig wlan0 down
ifconfig wlan0 up
sudo iwconfig wlan0 mode Managed essid $1 key $2
sudo dhclient -v wlan0

