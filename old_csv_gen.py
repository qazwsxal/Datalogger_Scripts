#!/bin/python3
"""
Created on Thu Mar 17 14:38:43 2016

Creates a csv file

@author: adam
"""
# import sys
import csv
import mysql.connector as sql
import motors
# import matplotlib.pyplot as plt
# import pytz
# import math
###############################################################################

###############################################################################
# mysql config
USERNAME = "root"
DATABASE = "test"
# HOST = "192.168.7.2"
HOST = "127.0.0.1"

PASSWORD = "dusc2015"

# time config
# localtime=pytz.timezone("Australia/Darwin")


MOTOR_BASE_ID = int("0x600", 16)
DRIVERBASE_ID = int("0x500", 16)


motor = motors.Wavesculptor20(MOTOR_BASE_ID)

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
with open('20160316.csv', 'w', newline='') as fp:
    a = csv.writer(fp, delimiter=',')
    headers = [motor.csv_headers]
    a.writerows(headers)
    for row in cursor:
        motor.parse_can_msg(row[2], row[3])
        # for k, v in motor.status().items():
        #    print(k,v)
        data = [[row[0]] + [row[1]] + motor.csv_data()]
        a.writerows(data)
