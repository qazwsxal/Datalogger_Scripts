#!/bin/python3
"""
Created on Thu 28 Apr 2016 17:36:32 BST

Logs CAN messages to mysql server

@author: Adam Leach adam.leach@dur.ac.uk, qazwsxalan@gmail.com
"""
# import sys
import datetime
import motors
from dbstorage import WS20_DOM
from dbstorage import Base
import sqlalchemy as sqla
from sqlalchemy.orm import sessionmaker
import can
# mysql config
USERNAME = "root"
DATABASE = "2016test"
# HOST = "192.168.7.2"
HOST = "127.0.0.1"
PASSWORD = "dusc2015"

serveraddr = "mysql+mysqlconnector://%s:%s@%s/%s" % (
    USERNAME, PASSWORD, HOST, DATABASE)
engine = sqla.create_engine(serveraddr, pool_recycle=3600)
motor_DOM = WS20_DOM()
Base.metadata.create_all(engine)
session_init = sessionmaker(bind=engine)
session = session_init()

# CAN config
MOTOR_BASE_ID = int("0x600", 16)
DRIVERBASE_ID = int("0x500", 16)

CAN_INTERFACE = 'can0'
CAN_INTERFACE_TYPE = 'socketcan_ctypes'

bus = can.interface.Bus(CAN_INTERFACE, CAN_INTERFACE_TYPE)

motor = motors.Wavesculptor20(MOTOR_BASE_ID)

while 1:
    msg = bus.recv()
    motor.parse_can_msg(msg.arbitration_id, msg.data)
    data = motor.status()
    data["time"] = datetime.datetime.now()
    session.add(WS20_DOM(**data))
    session.commit()
