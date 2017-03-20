import serial
import struct

VOLTAGE_FACTOR = 0.005
def parseResp(response):
    ans = struct.unpack('<BBHHHHHHHHHHBBBBBBB', response)
    moduleData = {}
    moduleData['ID'] = ans[0]
    moduleData['cellVolts'] = [x * VOLTAGE_FACTOR for x in ans[2:9:2]]
    moduleData['Cycles'] = ans[10]
    moduleData['OTP'] = ans[12]
    moduleData['OVP'] = ans[14]
    moduleData['LVP'] = ans[16]
    return moduleData

conn = serial.Serial('/dev/ttyUSB0', 600, parity=serial.PARITY_EVEN,
                     timeout=0.8)
cells = []
for i in range(35):
    msg = bytearray([129, 170, i, i])
    conn.write(msg)
    if len(conn.read(29)):
        cells.append(i)

while True:
    for i in cells:
        msg = bytearray([129, 170, i, i])
        conn.write(msg)
        data =parseResp(conn.read(29))
        print(data)

