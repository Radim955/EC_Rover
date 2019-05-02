#! /bin/sh
# Sets IP to ETHERNET and keeps it UP even after rebooting

/etc/network/interfaces

auto eth0
iface eth0 inet static
address 192.168.1.250
subnet 255.255.0.0
