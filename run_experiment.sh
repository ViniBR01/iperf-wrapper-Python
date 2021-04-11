#! /bin/bash

#Script to run larger experiments using the python wrapper of iperf3

filesize=300000 #B
runtime=60 #sec
mininterval=5.0 #sec
maxinterval=1.5 #sec

echo "Starting experiments!"

#python main.py
python main.py -i 192.168.0.102 -f $filesize -l $runtime -t $mininterval -g $maxinterval > test.txt &
# python main.py -i 192.168.0.103 -f $filesize -l $runtime -t $mininterval -g $maxinterval > test2.txt &
# python main.py -i 192.168.0.104 -f $filesize -l $runtime -t $mininterval -g $maxinterval > test3.txt &
# python main.py -i 192.168.0.105 -f $filesize -l $runtime -t $mininterval -g $maxinterval > test4.txt &
# python main.py -i 192.168.0.106 -f $filesize -l $runtime -t $mininterval -g $maxinterval > test5.txt &
# python main.py -i 192.168.0.107 -f $filesize -l $runtime -t $mininterval -g $maxinterval > test6.txt &

wait

echo "bye."