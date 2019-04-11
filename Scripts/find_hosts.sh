#! /bin/sh

echo ===================
echo = ARG1: IP/MASK
echo ===================

nmap -sP $1
