# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 13:31:48 2016

@author:  Adam Leach (adam.leach@durham.ac.uk, qazwsxalan@gmail.com)
"""
import struct


class Controls(object):
    """ Driver Controls CAN Class

    Keyword Arguments:
    controls_base_address -- Integer, Motor Controller's base address,
                       default 1280 (0x500)
    """
    def __init__(self, mc_base_address=1280):
        self.types = {mc_base_address:      "ID",   # Identification Info
                      mc_base_address + 1:  "Mtr",  # Motor Drive Command
                      mc_base_address + 2:  "Bus",  # Motor Power Command
                      mc_base_address + 3:  "Rst",  # Reset WaveSculptor
                      mc_base_address + 4:  "Swi"}  # Switch Status

        self.formats = {"ID":   "u_int32 & char[4]",  # Identification info.
                        "Swi":  "2*u_int32"}          # Switch Information
        #               control messages: 2*float32     Telemetry (standard)
        #               reset:  No data

        self.config = {"seriaNo": 12345}  # Not that important but worth having

        # Values grouped as they arrive over CAN bus
        self._cangroups = {"Mtr":          (0, 0),  # Motor Command
                           "Bus":          (0, 0),  # Bus Command
                           "Swi":          (0, 0)}  # Switch Status

        self.csv_headers = list(self.status().keys())

    def status(self):
        """returns a dict of driver commands"""
        statdict = {"busCurrent":      self._cangroups["Bus"][0],
                    "motorCurrent":    self._cangroups["Mtr"][0],
                    "motorVelocity":   self._cangroups["Mtr"][1]}
        return statdict

    def csv_data(self):
        """Returns a list of stats and flags for use in CSV exporting"""
        # There has to be a nicer way to do this...
        data = []
        for key in self.csv_headers:
            data.append(self.status()[key])
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

        elif msg_format == "2*u_int32":  # Switch Information
            pass  # TODO

        else:
            first, second = struct.unpack("ff", can_data)
            self._cangroups[msg_type] = (second, first)
        return 1

    def get_speed(self, units='km/h'):
        """ Returns desired speed of motor as a float.

        Keyword Arguments:
        units -- String
                 default: units="km/h"
                 valid: kph, km/h, m/s, mph
        """

        if units == 'km/h' or units == 'kph':
            speed = 3.6 * self._cangroups["Mtr"][1]
        elif units == 'mph':
            speed = 2.2369363 * self._cangroups["Mtr"][1]
        elif units == 'm/s':
            speed = float(self._cangroups["Mtr"][1])
        return speed
