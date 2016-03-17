DUEM Datalogger Scripts
=======================

**A collection of scripts for use on DUSC 2015's Beaglebone Black Datalogger**

##Setup

Run setup.sh after making sure it's executeable

```
chmod +x setup.sh
./setup.sh
```

This sets up the required packages for the python scripts to run correctly, this is done in a virtual environment so as not to mess up any other python packages on the system. This also installs the spyder IDE into the virtual environment for development purposes.

##Running

Python scripts need virtualenv to be active in order to run correctly `source .venv/bin/activate`
Run `spyder3` in the terminal after virtualenv activated in order to have the correct package versions loaded when developing/debugging.

Scripts can also be run by calling their respective shell scripts, this automatically sets up the virtualenv, which is particularly useful for scripts to be used in cron jobs, on startup, or otherwise called automatically (dmesg trigger?). 


## CANUSB caveats

The [CANUSB from LAWICEL](www.canusb.com) is a wonderful peice of equipment that easily connects to Tritium's awkward-to-find-connectors-for CAN network. It can be used as a SocketCAN interface the same way that the Beaglebone's onboard CAN transciever can. 

*To set up CANUSB as a CAN interface*
```
slcan_attach -f -o -s8 /dev/<CANUSB tty>
slcand /dev/<CANUSB tty> slcan0
ifconfig slcan0 up
```

However, voltage spikes and noise can cause the BBB to disconnect from the CANUSB. This seems to be due to a grounding issue or possibly a power draw problem. Minimising this can be done by removing the S99ondemand startup script from the rc2.d folder and adding `echo 'on' | tee /sys/bus/usb/devices/usb1/power/control` to /etc/rc.local. These keep the beaglebone running at full power and prevent it from turning off USB power respectively. (See [https://groups.google.com/forum/#!topic/beagleboard/C6gMT2\_FfiM](https://groups.google.com/forum/#!topic/beagleboard/C6gMT2_FfiM) for details)
