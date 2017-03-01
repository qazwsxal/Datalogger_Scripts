#!/bin/python3
"""
Created on Thu 28 Apr 2016 17:36:32 BST

Logs CAN messages to mysql server

@author: Adam Leach adam.leach@dur.ac.uk, qazwsxalan@gmail.com
"""
import sys
import datetime
import json
import sqlalchemy as sqla
from sqlalchemy.orm import sessionmaker
import motors
import controls
import dbstorage
from can.interfaces import socketcan_native as native_bus
# mysql config
username = "root"
database = "2016test"
# host = "192.168.7.2"
host = "127.0.0.1"
password = "dusc2015"
serveraddr = "mysql+mysqlconnector://%s:%s@%s/%s" % (
    username, password, host, database)

# can config
motor_base_id = int("0x600", 16)
driver_base_id = int("0x500", 16)
can_interface = sys.argv[1]
can_interface_type = 'socketcan_ctypes'
bus = native_bus.SocketscanNative_Bus(channel=can_interface)

# Set up bus objects
motor = motors.Wavesculptor20(mc_base_address=motor_base_id)
controls = controls.Controls(controls_base_address=driver_base_id)
can_objects = [motor, controls]


# Set up bus object ORM interfaces
can_orms = [dbstorage.WS20_ORM, dbstorage.Controls_ORM]

# Set up bus object shared memory files
motor_file = "/dev/shm/motor"
controls_file = "/dev/shm/controls"
can_files = [motor_file, controls_file]

# intial file setup prevents file not found errors

for i, active_obj in enumerate(can_objects):
    data = active_obj.status()
    data["time"] = datetime.datetime.now().isoformat()
    json.dump(data, open(can_files[i], "w"))

# mysql setup
engine = sqla.create_engine(serveraddr, pool_recycle=3600)
dbstorage.Base.metadata.create_all(engine)
session_init = sessionmaker(bind=engine)
session = session_init()


while 1:
    msg = bus.recv()
    for i, active_obj in enumerate(can_objects):
        if msg.arbitration_id in active_obj.can_range:
            # Get a copy of old data, update and count changes
            old_data = active_obj.status()
            active_obj.parse_can_msg(msg.arbitration_id, msg.data)
            data = active_obj.status()
            data["time"] = datetime.datetime.now().isoformat()
            changed = {}
            for key in old_data:
                # only log updated values, saves space.
                # SQLalchemy needs to be explicitly told a key is NULL
                if data[key] == old_data[key]:
                    changed[key] = None
                else:
                    changed[key] = data[key]
            changed["time"] = datetime.datetime.now()
            jsonfile = open(can_files[i], "w")
            json.dump(data, jsonfile)
            # print(data)
            jsonfile.close()
            active_orm = can_orms[i]
            session.add(active_orm(**changed))
            # Commiting every message might strain server,
            # setting transaction flushes to occur
            # once per second should help
            session.commit()
