#!/bin/python3
"""
Created on Thu Mar 17 14:38:43 2016

Database format migration, inserts into new schema

@author: adam
"""
import mysql.connector as sql
import motors
from dbstorage import WS20_DOM
from dbstorage import Base
import sqlalchemy as sqla
from sqlalchemy.orm import sessionmaker


USERNAME = "root"
DATABASE = "test"
NEW_DB = "test2"
# HOST = "192.168.7.2"
HOST = "127.0.0.1"
PASSWORD = "dusc2015"

# time config
# localtime=pytz.timezone("Australia/Darwin")


MOTOR_BASE_ID = int("0x600", 16)
DRIVERBASE_ID = int("0x500", 16)

serveraddr = "mysql+mysqlconnector://%s:%s@%s/%s" % (
    USERNAME, PASSWORD, HOST, NEW_DB)
engine = sqla.create_engine(serveraddr, pool_recycle=3600)
motor = motors.Wavesculptor20(MOTOR_BASE_ID)
motor_DOM = WS20_DOM()
Base.metadata.create_all(engine)
session_init = sessionmaker(bind=engine)
session = session_init()

start_time = '2015-18-16 00:00:48'
end_time = '2016-10-17 04:18:48'


# Charge count message ID's
# connect to db
connect = sql.connect(user=USERNAME,
                      password=PASSWORD,
                      database=DATABASE,
                      host=HOST)
cursor = connect.cursor()
# Get latest entry in charge table
get_newer_charges = ("SELECT msg_no, msg_time, msg_id, msg_data "
                     "FROM can "
                     "WHERE msg_id <= 1550 "
                     "AND msg_id >= 1536 "
                     "ORDER BY msg_no ASC;")

print(get_newer_charges)
cursor.execute(get_newer_charges)

# Next bit takes a while...
for row in cursor:
    motor.parse_can_msg(row[2], row[3])
    # for k, v in motor.status().items():
    #    print(k,v)
    data = motor.status()
    data["time"] = row[1]
    session.add(WS20_DOM(**data))
session.commit()
