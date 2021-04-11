#! /bin/bash

#Script to run larger experiments using the python wrapper of iperf3

filesize=300000 #B
runtime=5 #sec
mininterval=1.5 #sec
maxinterval=0.5 #sec

echo "Starting experiments!"

#python main.py
python main.py -i 192.168.0.102 -f $filesize -l $runtime -t $mininterval -g $maxinterval > test.txt

echo "bye."