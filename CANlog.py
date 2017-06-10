#!/bin/python3
"""
Created on Thu 28 Apr 2016 17:36:32 BST

Logs CAN messages to mysql server

@author: Adam Leach adam.leach@dur.ac.uk, qazwsxalan@gmail.com
"""
import controls
import datetime
import dbstorage
import json
import motors
import os
import sqlalchemy as sqla
import sys
import time
import threading
import queue
from can.interfaces import socketcan_native as native_bus
from sqlalchemy.orm import sessionmaker


def mysql_worker(session, canQueue):
    while True:
        item = canQueue.get()
        if item is None:
            session.commit()
        session.add(item)
        if time.clock() % COMMIT_RATE < 1.0:
            session.commit()


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

COMMIT_RATE = 60

msg_queue = queue.Queue()

threading.thread(target=mysql_worker, args=(session, msg_queue))
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
            jsonfile.flush()
            os.fsync(jsonfile.fileno())
            jsonfile.close()
            active_orm = can_orms[i]
            msg_queue.put(active_orm(**changed))
            # Commiting every message might strain server,
            # setting transaction flushes to occur
            # once per second should help
