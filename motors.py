# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 13:31:48 2016

@author:  Adam Leach (adam.leach@durham.ac.uk, qazwsxalan@gmail.com)
"""
import struct


class Wavesculptor20(object):
    """ Tritium Motor Controller Class

    Keyword Arguments:
    mc_base_address -- Integer, Motor Controller's base address,
                       default 1536 (0x600)
    """
    def __init__(self, mc_base_address=1536):
        self.types = {mc_base_address:      "ID",   # Identification Info
                      mc_base_address + 1:  "Sts",  # Staus Information
                      mc_base_address + 2:  "Bus",  # Bus (Amps + Volts)
                      mc_base_address + 3:  "Vel",  # Velocity (m/s + rpm)
                      mc_base_address + 4:  "PhC",  # Phase Current
                      mc_base_address + 5:  "MVV",  # Motor Voltage Vector
                      mc_base_address + 6:  "MVC",  # Motor Current Vector
                      mc_base_address + 7:  "MBE",  # Motor BackEMF Vector
                      mc_base_address + 8:  "VR1",  # 15 & 1.65 Volt. Rail
                      mc_base_address + 9:  "VR2",  # 2.5 & 1.2 Volt. Rail
                      mc_base_address + 10: "FSM",  # Fan Speed Measrement
                      mc_base_address + 11: "SKT",  # Sink & Motor Temperature
                      mc_base_address + 12: "ICT",  # Air In & CPU Temperature
                      mc_base_address + 13: "OCT",  # Air Out & Cap Temperature
                      mc_base_address + 14: "ODO"}  # Odo. & Bus AmpHours

        self.can_range = range(mc_base_address, mc_base_address+15)

        self.formats = {"ID":    "u_int32 & char[4]",  # Identification info.
                        "Sts":  "3*u_int16"}           # Staus Information
        #               all other messages: 2*float32    Telemetry (standard)

        self.config = {"seriaNo": 12345,  # These aren't that important but
                       "activeMotor": 0}  # worth having for full WS20 spec.

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

        # Values grouped as they arrive over CAN bus
        self._cangroups = {"Bus":          (0, 0),  # Bus Measurement
                           "PhC":          (0, 0),  # Velocity Measrement
                           "Vel":          (0, 0),  # Velocity Measrement
                           "MVV":          (0, 0),  # Motor Voltage Vector Meas
                           "MVC":          (0, 0),  # Motor Current Vector Meas
                           "MBE":          (0, 0),  # Motor BackEMF Vector Meas
                           "VR1":          (0, 0),  # 15 & 1.65 Volt. Rail Meas
                           "VR2":          (0, 0),  # 2.5 & 1.2 Volt. Rail Meas
                           "FSM":          (0, 0),  # Fan Speed Measrement
                           "SKT":          (0, 0),  # Sink & Motor Temp. Meas
                           "ICT":          (0, 0),  # Air In & CPU Temp. Meas
                           "OCT":          (0, 0),  # Air out & Cap Temp. Meas
                           "ODO":          (0, 0)}  # Odo. & Bus AmpHours Meas

        self.csv_headers = list(self.status().keys()) + \
            list(self.limits.keys()) + \
            list(self.errors.keys())

    def status(self):
        """returns a dict of motor status"""
        # Rewrite using python getter + @property decorator
        # motor.status shouldn't be a function call, feels weird.
        statdict = {"busCurrent":        self._cangroups["Bus"][0],
                    "busVoltage":        self._cangroups["Bus"][1],
                    "vehicleVelocity":   self._cangroups["Vel"][0],
                    "motorVelocity":     self._cangroups["Vel"][1],
                    "phaseACurrent":     self._cangroups["PhC"][0],
                    "phaseBCurrent":     self._cangroups["PhC"][1],
                    "vectVoltReal":      self._cangroups["MVV"][0],
                    "vectVoltImag":      self._cangroups["MVV"][1],
                    "vectCurrReal":      self._cangroups["MVC"][0],
                    "vectCurrImag":      self._cangroups["MVC"][1],
                    "backEMFReal":       self._cangroups["MBE"][0],
                    "backEMFImag":       self._cangroups["MBE"][1],
                    "fifteenVsupply":    self._cangroups["VR1"][0],
                    "onesixfiveVsupply": self._cangroups["VR1"][1],
                    "twofiveVsupply":    self._cangroups["VR2"][0],
                    "onetwoVsupply":     self._cangroups["VR2"][1],
                    "fanSpeed":          self._cangroups["FSM"][0],
                    "fanDrive":          self._cangroups["FSM"][1],
                    "heatSinkTemp":      self._cangroups["SKT"][0],
                    "motorTemp":         self._cangroups["SKT"][1],
                    "airInletTemp":      self._cangroups["ICT"][0],
                    "processorTemp":     self._cangroups["ICT"][1],
                    "airOutletTemp":     self._cangroups["OCT"][0],
                    "capacitorTemp":     self._cangroups["OCT"][1],
                    "DCBusAmpHours":     self._cangroups["ODO"][0],
                    "Odometer":          self._cangroups["ODO"][1]}
        return statdict

    def csv_data(self):
        """Returns a list of stats and flags for use in CSV exporting"""
        # There has to be a nicer way to do this...
        data = []
        for key in self.csv_headers:
            try:
                data.append(self.status()[key])
            except KeyError:
                try:
                    data.append(self.limits[key])
                except KeyError:
                    data.append(self.errors[key])
        return data

    def parse_can_msg(self, can_id, can_data):
        """Parses CAN msg, from SQL db or CAN Network, updates internal state

        Returns true if ID matches.
        Arguments:
        can_id   -- Integer, message ID from CAN network, determines frame type
        can_data -- Raw bits from CAN Data field, frame type tells us format
        """
        try:
            msg_type = self.types[can_id]
        except KeyError:
            return 0
        try:
            msg_format = self.formats[msg_type]
        except KeyError:
            msg_format = "2*float32"

        if msg_format == "u_int32 + char[4]":  # Identification information
            pass   # These Values should not change

        elif msg_format == "3*u_int16":  # Status Information
            '''
            # Just rewrite this entire, awful, section. It never worked.
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
            self._cangroups[msg_type] = (second, first)
        return 1

    def get_speed(self, units='km/h'):
        """ Returns speed of motor as a float.

        Keyword Arguments:
        units -- String
                 default: units="km/h"
                 valid: kph, km/h, m/s, mph
        """

        if units == 'km/h' or units == 'kph':
            speed = 3.6 * self._cangroups["Vel"][0]
        elif units == 'mph':
            speed = 2.2369363 * self._cangroups["Vel"][0]
        elif units == 'm/s':
            speed = float(self._cangroups["Vel"][0])
        return speed
