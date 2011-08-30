#!/bin/bash

cd /home/mediamatic/work/banjo/code/printer
./print $1 &

sleep 45

mv $1 ../../output/printed

kill `cat /tmp/emulator.pid`
echo "doeg!!"

ps aux|grep python
