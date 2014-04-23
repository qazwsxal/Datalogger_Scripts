#!/bin/bash

# enable can0
# sudo ip link set can0 down
# sudo ip link set can0 type can bitrate 1000000
# sudo ip link set can0 up

# enable slcan0
slcand -o -c -f -s8 /dev/ttyUSB0 slcan0
ifconfig slcan0 up

# activate venv
source /root/Datalogger_Scripts/.venv/bin/activate

# run CANlog.py
python3 /root/Datalogger_Scripts/CANlog.py slcan0
