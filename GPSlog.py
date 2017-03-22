import dbstorage
import json
import os
import sqlalchemy as sqla
import time
from sqlalchemy.orm import sessionmaker
from gps3 import gps3


# mysql config
username = "root"
database = "2016test"
# host = "192.168.7.2"
host = "127.0.0.1"
password = "dusc2015"
serveraddr = "mysql+mysqlconnector://%s:%s@%s/%s" % (
    username, password, host, database)


# set up gps
gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()
gps_orm = dbstorage.GPS_ORM
gps_file = "/dev/shm/gps"

# mysql setup
engine = sqla.create_engine(serveraddr, pool_recycle=3600)
dbstorage.Base.metadata.create_all(engine)
session_init = sessionmaker(bind=engine)
session = session_init()

for new_data in gps_socket:
    starttime = time.time()
    if new_data:
        old = data_stream.TPV.copy()
        data_stream.unpack(new_data)
        session.add(gps_orm(**data_stream.TPV))
        session.commit()
        jsonfile = open(gps_file, "w+")
        json.dump(data_stream.TPV, jsonfile)
        jsonfile.flush()
        os.fsync(jsonfile.fileno())
        jsonfile.close
        # sleep for a second
        time.sleep(1.0 - ((time.time() - starttime) % 1.0))
