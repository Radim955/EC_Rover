# EC_Rover

Epic Challenge Rover base

This document is messy and unfinished. Currently just a sketch/memo

# Setup

Install and configure nginx with PHP and enable symlinks
set: root /home/pi/ec_rover/http;


Install and configure ser2net
apt-get install ser2net

/etc/ser2net.conf:
57574:http:60000:/dev/ttyUSB0:115200 8DATABITS NONE 1STOPBIT -XONXOFF -RTSCTS -LOCAL -HANGUP_WHEN_DONE


Install MJPEG Streamer
https://github.com/jacksonliam/mjpg-streamer

Running windowed
Also autostarted using this @ ~/.config/autostart/rover_server.desktop
lxterminal -l --working-directory='/home/pi/ec_rover' -e '/bin/sh -c ./startup.sh'
