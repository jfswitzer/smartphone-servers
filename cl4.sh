#!/bin/bash
powerstat -z -d 0 0.5 960 >> 4_pstat$1.out &
sleep 60;
yes > /dev/null & sudo cpulimit -p $! --limit $1 &
yes > /dev/null & sudo cpulimit -p $! --limit $1 &
yes > /dev/null & sudo cpulimit -p $! --limit $1 &
yes > /dev/null & sudo cpulimit -p $! --limit $1 & sleep 360;
pkill yes;
sleep 60
