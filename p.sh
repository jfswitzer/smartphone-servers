powerstat -z -d 0 0.5 960 >> pstat.out &
sleep 30;
yes > /dev/null & yes > /dev/null & yes > /dev/null & yes > /dev/null &
sleep 360;
pkill yes;
sleep 30
