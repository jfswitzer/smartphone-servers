#!/bin/bash
powerstat -z -d 0 0.5 960 >> 20_pstat2.out &
sleep 60;
yes > /dev/null & sudo cpulimit -p $! --limit 20 &
yes > /dev/null & sudo cpulimit -p $! --limit 20 & sleep 360;
pkill yes;
sleep 60;

powerstat -z -d 0 0.5 960 >> 40_pstat2.out &
sleep 60;
yes > /dev/null & sudo cpulimit -p $! --limit 40 &
yes > /dev/null & sudo cpulimit -p $! --limit 40 & sleep 360;
pkill yes;
sleep 60;

powerstat -z -d 0 0.5 960 >> 60_pstat2.out &
sleep 60;
yes > /dev/null & sudo cpulimit -p $! --limit 60 &
yes > /dev/null & sudo cpulimit -p $! --limit 60 & sleep 360;
pkill yes;
sleep 60;

powerstat -z -d 0 0.5 960 >> 80_pstat2.out &
sleep 60;
yes > /dev/null & sudo cpulimit -p $! --limit 80 &
yes > /dev/null & sudo cpulimit -p $! --limit 80 & sleep 360;
pkill yes;
sleep 60;

powerstat -z -d 0 0.5 960 >> 100_pstat2.out &
sleep 60;
yes > /dev/null & sudo cpulimit -p $! --limit 100 &
yes > /dev/null & sudo cpulimit -p $! --limit 100 & sleep 360;
pkill yes;
sleep 60;
