#! /bin/sh
# Searches for WIFIs available

sudo iw dev wlan0 scan | grep SSID
