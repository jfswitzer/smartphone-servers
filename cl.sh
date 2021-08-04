#!/bin/bash
powerstat -z -d 0 0.5 960 >> pstat$1.out &
sleep 30;
yes > /dev/null & sudo cpulimit -p $! --limit $1 & sleep 360;
pkill yes;
sleep 30
