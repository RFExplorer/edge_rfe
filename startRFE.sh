#!/bin/sh 
SERVICE="RFE.py"
if ps ax | grep -v grep | grep -v $0 | grep $SERVICE > /dev/null
then
    logger "$SERVICE service running, no action"
else
    logger "$SERVICE is not running"
    sudo python /home/pi/PythonProjects/RFEv2.0/RFE.py &
    logger "Started $SERVICE..."
fi
