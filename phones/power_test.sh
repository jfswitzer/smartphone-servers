powerstat -z -d 0 0.5 960 >> pstat.out &
python3 send_heartbeat.py &
python3 client.py;
