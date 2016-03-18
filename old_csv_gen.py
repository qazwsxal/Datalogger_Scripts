#!/bin/python3
"""
Created on Thu Mar 17 14:38:43 2016

Creates a csv file 

@author: adam
"""
import sys
import mysql.connector as sql
import csv
import motors
#import matplotlib.pyplot as plt
#import pytz
#import math
###############################################################################

###############################################################################
#mysql config
username="root"
database="test"
#host="192.168.7.2"
host="127.0.0.1"

password="dusc2015"

#time config
#localtime=pytz.timezone("Australia/Darwin")


motorbase_ID = int("0x600",16) 
driverbase_ID= int("0x500",16)


motor = motors.Tritium(motorbase_ID)

start_time = '2015-18-16 00:00:48'
end_time = '2016-10-17 04:18:48'


#Charge count message ID's
#connect to db
connect = sql.connect(user=username,password=password,database=database,host=host)
cursor = connect.cursor()
# Get latest entry in charge table
get_newer_charges= "SELECT msg_no, msg_time, msg_id, msg_data FROM can where msg_id <=1550 AND msg_id >= 1536 ORDER BY msg_no ASC;"
print(get_newer_charges)
cursor.execute(get_newer_charges)
with open('test.csv', 'w', newline='') as fp:
    a = csv.writer(fp, delimiter=',')
    headers= [["msg_ID",
               "Time",
               "busCurrent",
               "busVoltage",
               "vehicleVelocity",
               "motorVelocity",
               "phaseACurrent",
               "phaseBCurrent",
               "vectVoltReal",
               "vectVoltImag",
               "vectCurrReal",
               "vectCurrImag",
               "backEMFReal",
               "backEMFImag",
               "fifteenVsupply",
               "onesixfiveVsupply",
               "twofiveVsupply",
               "onetwoVsupply",
               "fanSpeed",
               "fanDrive",
               "heatSinkTemp",
               "motorTemp",
               "airInletTemp",
               "processorTemp",
               "airOutletTemp",
               "capacitorTemp",
               "DCBusAmpHours",
               "Odometer"]]
    a.writerows(headers)
    for row in cursor:
        motor.parseoldSQL(row)
        data = [[motor.ID               ,
                 motor.time             ,
                 motor.busCurrent       ,
                 motor.busVoltage       ,
                 motor.vehicleVelocity  ,
                 motor.motorVelocity    ,
                 motor.phaseACurrent    ,
                 motor.phaseBCurrent    ,
                 motor.vectVoltReal     ,
                 motor.vectVoltImag     ,
                 motor.vectCurrReal     ,
                 motor.vectCurrImag     ,
                 motor.backEMFReal      ,   #0 by definition
                 motor.backEMFImag      ,
                 motor.fifteenVsupply   ,
                 motor.onesixfiveVsupply,
                 motor.twofiveVsupply   ,
                 motor.onetwoVsupply    ,
                 motor.fanSpeed         ,
                 motor.fanDrive         ,
                 motor.heatSinkTemp     ,
                 motor.motorTemp        ,
                 motor.airInletTemp     ,
                 motor.processorTemp    ,
                 motor.airOutletTemp    ,
                 motor.capacitorTemp    ,
                 motor.DCBusAmpHours    ,
                 motor.Odometer
        ]]
        a.writerows(data)