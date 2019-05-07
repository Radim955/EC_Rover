#!/bin/bash

sudo /usr/local/sbin/ser2net -c ../ser2net.conf -P /run/ser2net.pid -d &
sudo /usr/local/bin/mjpg_streamer -o "output_http.so -p 9003" -i "input_uvc.so -q 30 -r 200x100 -y -f 15 -d /dev/video1" &
sudo /usr/local/bin/mjpg_streamer -o "output_http.so -p 9001" -i "input_uvc.so -q 30 -r 200x100 -y -f 15 -d /dev/video0" &
#/usr/local/bin/mjpg_streamer -o "output_http.so -p 9003" -i "input_uvc.so -q 30 -r 800x600 -y -f 15 -d /dev/video1" &

read
sudo killall -9 ser2net
sudo killall -9 mjpg_streamer
