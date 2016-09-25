#!/bin/bash

# enable can0
# sudo ip link set can0 down
# sudo ip link set can0 type can bitrate 1000000
# sudo ip link set can0 up

# Wait until ttyCAN exists
while [ ! -L /dev/ttyCAN ]; do sleep 1; echo notfound; done
echo found

# enable slcan0
slcand -o -c -f -s8 /dev/ttyCAN slcan0 > /root/Datalogger_Scripts/slcand_errors.txt
ifconfig slcan0 up > /root/Datalogger_Scripts/ifconfig_errors.txt

# activate venv
		source /root/Datalogger_Scripts/.venv/bin/activate

# run CANlog.py
python3 /root/Datalogger_Scripts/CANlog.py slcan0
