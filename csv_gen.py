#!/bin/python3
"""
Created on Thu Mar 17 14:38:43 2016

Creates a csv file 

@author: adam
"""
import sys
import mysql.connector as sql
import struct
import csv
#import matplotlib.pyplot as plt
#import pytz
#import math
#########################################################################################################################

#mysql config
username="root"
database="test"
#host="192.168.7.2"
host="127.0.0.1"

password="dusc2015"

#time config
#localtime=pytz.timezone("Australia/Darwin")


motorbase_ID = "0x600"
driverbase_ID= "0x500"
offset = 2

msg_id = int(motorbase_ID,16) + offset
start_time = '2015-18-16 00:00:48'
end_time = '2016-10-17 04:18:48'


#Charge count message ID's
#connect to db
connect = sql.connect(user=username,password=password,database=database,host=host)
cursor = connect.cursor()
# Get latest entry in charge table
get_newer_charges= "SELECT msg_no, msg_data, msg_time FROM can ORDER BY msg_no DESC LIMIT 20000;"
print(get_newer_charges)
cursor.execute(get_newer_charges)
candata = cursor.fetchall()

if candata:
    t1=[]
    t2=[]
    time = []
    for row  in candata:
        #print row
        t1.append(struct.unpack("ff", str(row[1]))[0])  #CHANGE IN LIVE VERSION
        t2.append(struct.unpack("ff", str(row[1]))[1])
        time.append(row[0])
connect.commit()

offset = 4
msg_id = int(motorbase_ID,16) + offset

get_newer_charges= "SELECT msg_no, msg_data, msg_time FROM can WHERE msg_id = \'"+str(msg_id)+ "\' ORDER BY msg_no DESC LIMIT 20000;"
cursor.execute(get_newer_charges)
candata = cursor.fetchall()

if candata:
    t3=[]
    t4=[]
    time2 = []
    for row  in candata:
        #print row
        t3.append(struct.unpack("ff", str(row[1]))[0])
        t4.append(struct.unpack("ff", str(row[1]))[1])  #CHANGE IN LIVE VERSION
        time2.append(row[0])
connect.commit()

offset = 1
msg_id = int(driverbase_ID,16) + offset


get_newer_charges= "SELECT msg_no, msg_data FROM can WHERE msg_id = "+str(msg_id)+ " ORDER BY msg_no DESC LIMIT 20000;"
cursor.execute(get_newer_charges)
#print(get_newer_charges)
candata = cursor.fetchall()
if candata:
    targ_curr=[]
    targ_speed=[]
    time3 = []
    for row  in candata:
        targ_curr.append(struct.unpack("ff", str(row[1]))[1])
        targ_speed.append(struct.unpack("ff", str(row[1]))[0])
        time3.append(row[0])
connect.commit()

#print(len(t1))
#fig, ax = plt.subplots()
#ax.plot(time, t1)
#ax.plot_date(time, t2, '-',tz=localtime)
#ax.plot(time2, t3)
#ax.plot(time2, t4)
#ax.plot(time3,targ_curr)
#ax.plot(time3,targ_speed)

# format the ticks
#ax.autoscale_view()

# format the coords message box
#fig.autofmt_xdate()
#plt.show()
