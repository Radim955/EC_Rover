#!/bin/bash

/usr/local/sbin/ser2net -c ser2net.conf -P /run/ser2net.pid -d &
/usr/local/bin/mjpg_streamer -o "output_http.so -p 9001" -i "input_uvc.so -q 30 -r 640x480 -y -f 15 -d /dev/video0" &
read
killall -9 ser2net
killall -9 mjpg_streamer
