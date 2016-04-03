# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 13:31:48 2016

@author:  Adam Leach (adam.leach@durham.ac.uk, qazwsxalan@gmail.com)
"""
import struct


class Tritium(object):
    """ Tritium Motor Controller Class

    Keyword Arguments:
    mc_base_address -- Integer, Motor Controller's base address,
                     default 1536 (0x600)
    """
    def __init__(self, mc_base_address=1536):
        self.types = {mc_base_address:      "ID",    # Identification Info
                      mc_base_address + 1:  "Stat",  # Status Information
                      mc_base_address + 2:  "Bus",   # Bus Measrement
                      mc_base_address + 3:  "Vel",   # Velocity Measrement
                      mc_base_address + 4:  "PhC",   # Phase Current Measrement
                      mc_base_address + 5:  "MVV",   # Motor Voltage Vector
                      mc_base_address + 6:  "MVC",   # Motor Current Vector
                      mc_base_address + 7:  "MBE",   # Motor BackEMF Vector
                      mc_base_address + 8:  "VR1",   # 15 & 1.65 Volt. Rail
                      mc_base_address + 9:  "VR2",   # 2.5 & 1.2 Volt. Rail
                      mc_base_address + 10: "FSM",   # Fan Speed Measrement
                      mc_base_address + 11: "SKT",   # Sink & Motor Temp. Meas
                      mc_base_address + 12: "ICT",   # Air In & CPU Temp. Meas
                      mc_base_address + 13: "OCT",   # Air out & Cap Temp. Meas
                      mc_base_address + 14: "ODO"}   # Odo. & Bus AmpHours

        self.formats = {"ID": "u_int32 + char[4]",  # Identification info.
                        "Stat": "3*u_int16"}        # Status Information
        # Else: 2 floats

        self.serial_number = 12345    # Not sure
        self.active_motor = 0
        # Flags inidicating errors
        self.errors = {"15VUVL":  0,  # A 15V rail under volt lock out occurred
                       "Conf":    0,  # Config Read Error
                       "Watch":   0,  # Watchdog caused last reset
                       "Halls":   0,  # Bad motor position hall sequence
                       "DCBusOV": 0,  # DC Bus over voltage
                       "SoftOC":  0,  # Software over current
                       "HardOC":  0}  # Hardware over current

        # Flags indicate limiting control loop
        self.limits = {"HeatS":  0,   # Heatink Temperature
                       "BusVL":  0,   # Bus Voltage Lower Limit
                       "BusVU":  0,   # Bus Voltage Upper Limit
                       "BusC":   0,   # Bus Current
                       "Velo":   0,   # Velocity
                       "MotorC": 0,   # Motor Current
                       "PWM":    0}   # Bridge PWM

        self.status = {"busCurrent":        0,
                       "busVoltage":        0,
                       "vehicleVelocity":   0,
                       "motorVelocity":     0,
                       "phaseACurrent":     0,
                       "phaseBCurrent":     0,
                       "vectVoltReal":      0,
                       "vectVoltImag":      0,
                       "vectCurrReal":      0,
                       "vectCurrImag":      0,
                       "backEMFReal":       0,    # 0 , by definition
                       "backEMFImag":       0,
                       "fifteenVsupply":    0,
                       "onesixfiveVsupply": 0,
                       "twofiveVsupply":    0,
                       "onetwoVsupply":     0,
                       "fanSpeed":          0,
                       "fanDrive":          0,
                       "heatSinkTemp":      0,
                       "motorTemp":         0,
                       "airInletTemp":      0,
                       "processorTemp":     0,
                       "airOutletTemp":     0,
                       "capacitorTemp":     0,
                       "DCBusAmpHours":     0,
                       "Odometer":          0}

        self.csv_headers = list(self.status.keys()) + \
            list(self.limits.keys()) + \
            list(self.errors.keys())

    def csv_data(self):
        """Returns a list of stats and flags for use in CSV exporting"""
        data = []
        for key in self.csv_headers:
            try:
                data.append(self.status[key])
            except:
                try:
                    data.append(self.limits[key])
                except:
                    data.append(self.errors[key])
        return data

    def parse_can_msg(self, can_id, can_data):
        """Parses CAN msg, from SQL db or CAN Network

        Arguments:
        can_id   -- Integer, message ID from CAN network, determines frame type
        can_data -- Raw bits from CAN Data field, frame type tells us format
    """
        msg_type = self.types[can_id]
        try:
            msg_format = self.formats[msg_type]
        except:
            msg_format = "2*float32"

        if msg_format == "u_int32 + char[4]":  # Identification information
            pass   # These Values should not change

        elif msg_format == "3*u_int16":  # Status Information
            '''
            self.a = [0,0,0,0,0,0,0,0]
            self.b = [0,0,0,0,0,0,0,0]
            #Awful hacky bit flags
            self.a,self.b,self.c,self.d = struct.unpack("hhhh",can_data)
            self.limits["HeatS"]        = bin(self.a)[0]
            self.limits["BusVL"]        = bin(self.a)[1]
            self.limits["BusVU"]        = bin(self.a)[2]
            self.limits["BusC"]         = bin(self.a)[3]
            self.limits["Velo"]         = bin(self.a)[4]
            self.limits["MotorC"]       = bin(self.a)[5]
            self.limits["PWM"]          = bin(self.a)[6]


            self.errors["15VUVL"]  = bin(self.b)[-7]
            self.errors["Conf"]    = bin(self.b)[-6]
            self.errors["Watch"]   = bin(self.b)[-5]
            self.errors["Halls"]   = bin(self.b)[-4]
            self.errors["DCBusOV"] = bin(self.b)[-3]
            self.errors["SoftOC"]  = bin(self.b)[-2]
            self.errors["HardOC"]  = bin(self.b)[-1]

            self.activeMotor = self.c
            '''
        else:
            first, second = struct.unpack("ff", can_data)
            if msg_type == "Bus":              # Bus Measurement
                self.status["busCurrent"] = second
                self.status["busVoltage"] = first

            elif msg_type == "Vel":            # Velocity Measrement
                self.status["vehicleVelocity"] = second
                self.status["motorVelocity"] = first

            elif msg_type == "PhC":            # Phase Current Measrement
                self.status["phaseACurrent"] = second
                self.status["phaseBCurrent"] = first

            elif msg_type == "MVV":            # Motor Voltage Vector Meas
                self.status["vectVoltReal"] = second
                self.status["vectVoltImag"] = first

            elif msg_type == "MVC":            # Motor Current Vector Meas
                self.status["vectCurrReal"] = second
                self.status["vectCurrImag"] = first

            elif msg_type == "MBE":            # Motor BackEMF Vector Meas
                self.status["backEMFReal"] = second
                self.status["backEMFImag"] = first

            elif msg_type == "VR1":            # 15 & 1.65 Volt. Rail Meas
                self.status["fifteenVsupply"] = second
                self.status["onesixfiveVsupply"] = first

            elif msg_type == "VR2":            # 2.5 & 1.2 Volt. Rail Meas
                self.status["twofiveVsupply"] = second
                self.status["onetwoVsupply"] = first

            elif msg_type == "FSM":            # Fan Speed Measrement
                self.status["fanSpeed"] = second
                self.status["fanDrive"] = first

            elif msg_type == "SKT":            # Sink & Motor Temp. Meas
                self.status["heatSinkTemp"] = second
                self.status["motorTemp"] = first

            elif msg_type == "ICT":            # Air In & CPU Temp. Meas
                self.status["airInletTemp"] = second
                self.status["processorTemp"] = first

            elif msg_type == "OCT":            # Air out & Cap Temp. Meas
                self.status["airOutletTemp"] = second
                self.status["capacitorTemp"] = first

            elif msg_type == "ODO":             # Odo. & Bus AmpHours Meas
                self.status["DCBusAmpHours"] = second
                self.status["Odometer"] = first
