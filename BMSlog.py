import datetime
import dbstorage
import json
import os
import serial
import sqlalchemy as sqla
import struct
import sys
from sqlalchemy.orm import sessionmaker
# mysql config
username = "root"
database = "2016test"
host = "127.0.0.1"
password = "dusc2015"
serveraddr = "mysql+mysqlconnector://%s:%s@%s/%s" % (
    username, password, host, database)

# mysql setup
bms_orm = dbstorage.BMS_ORM
engine = sqla.create_engine(serveraddr, pool_recycle=3600)
dbstorage.Base.metadata.create_all(engine)
session_init = sessionmaker(bind=engine)
session = session_init()

bms_file = "/dev/shm/bms"


VOLTAGE_FACTOR = 0.005


def parseResp(response):
    ans = struct.unpack('<BBHHHHHHHHHHBBBBBBB', response)
    moduleData = {}
    moduleData['modID'] = ans[0]
    moduleData['cellV0'] = VOLTAGE_FACTOR * ans[2]
    moduleData['cellV1'] = VOLTAGE_FACTOR * ans[4]
    moduleData['cellV2'] = VOLTAGE_FACTOR * ans[6]
    moduleData['cellV3'] = VOLTAGE_FACTOR * ans[8]
    moduleData['cycles'] = ans[10]
    moduleData['OTP'] = ans[12]
    moduleData['OVP'] = ans[14]
    moduleData['LVP'] = ans[16]
    return moduleData


conn = serial.Serial('/dev/ttyBMS', 600, parity=serial.PARITY_EVEN,
                     timeout=0.8)
cells = []
batterypack = {}
for i in range(35):
    msg = bytearray([129, 170, i, i])
    conn.write(msg)
    if len(conn.read(29)):
        cells.append(i)
        print("module", i, "found")

while True:
    for i in cells:
        msg = bytearray([129, 170, i, i])
        conn.write(msg)
        data = parseResp(conn.read(29))
        data["time"] = datetime.datetime.now().isoformat()
        session.add(bms_orm(**data))
        session.commit()
        batterypack[data['modID']] = data
        jsonfile = open(bms_file, "w+")
        json.dump(batterypack, jsonfile)
        jsonfile.flush()
        os.fsync(jsonfile.fileno())
        jsonfile.close
