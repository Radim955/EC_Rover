#!/bin/sh

sudo /usr/local/sbin/ser2net -c ser2net.conf -P /run/ser2net.pid -d > /home/pi/ec_rover/ser2net_log 2>&1 &
sudo /usr/local/bin/mjpg_streamer -o "output_http.so -p 9003" -i "input_uvc.so -q 30 -r 200x100 -y -f 15 -d /dev/video1" &
sudo /usr/local/bin/mjpg_streamer -o "output_http.so -p 9001" -i "input_uvc.so -q 30 -r 200x100 -y -f 15 -d /dev/video0" &
