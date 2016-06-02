#!/bin/python3
"""
Created on Thu 28 Apr 2016 17:36:32 BST

Logs CAN messages to mysql server

@author: Adam Leach adam.leach@dur.ac.uk, qazwsxalan@gmail.com
"""
import sys
import datetime
import sqlalchemy as sqla
from sqlalchemy.orm import sessionmaker
import motors
import controls
import dbstorage
import can
# mysql config
username = "root"
database = "2016test"
# host = "192.168.7.2"
host = "127.0.0.1"
password = "dusc2015"


# can config
motor_base_id = int("0x600", 16)
driver_base_id = int("0x500", 16)
can_interface = sys.argv[1]
can_interface_type = 'socketcan_ctypes'

bus = can.interface.bus(can_interface, can_interface_type)

serveraddr = "mysql+mysqlconnector://%s:%s@%s/%s" % (
    username, password, host, database)
engine = sqla.create_engine(serveraddr, pool_recycle=3600)

motor = motors.Wavesculptor20(mc_base_address=motor_base_id)
controls = controls.Controls(controls_base_address=driver_base_id)
can_objects = [motor, controls]

motor_dom = dbstorage.WS20_DOM()
controls_dom = dbstorage.Controls_DOM()
can_doms = [motor_dom, controls_dom]

dbstorage.Base.metadata.create_all(engine)
session_init = sessionmaker(bind=engine)
session = session_init()


while 1:
    msg = bus.recv()
    for i, active_obj in enumerate(can_objects):
        if msg.arbitration_id in active_obj.active_range:
            old_data = active_obj.status()
            active_obj.parse_active_msg(msg.arbitration_id, msg.data)
            data = active_obj.status()
            changed = {}
            for key in old_data:
                if data[key] == old_data[key]:
                    changed[key] = None  # takes up less space in SQL
                else:
                    changed[key] = data[key]
            changed["time"] = datetime.datetime.now()
            active_dom = can_doms[i]
            session.add(active_dom(**changed))
            session.commit()
