# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 13:31:48 2016

@author: adam
"""
import struct

class Tritium:    
    
    def __init__(self,MCBaseAdress):
        self.MCBaseAdress = MCBaseAdress
        self.types   = {MCBaseAdress     : "ID",    #Identification information
                        MCBaseAdress +  1: "Stat",  #Status Information
                        MCBaseAdress +  2: "Bus",   #Bus Measurement   
                        MCBaseAdress +  3: "Vel",   #Velocity Measurement
                        MCBaseAdress +  4: "PhC",   #Phase Current Measurement
                        MCBaseAdress +  5: "MVV",   #Motor Voltage Vector Meas.
                        MCBaseAdress +  6: "MVC",   #Motor Current Vector Meas.                       
                        MCBaseAdress +  7: "MBE",   #Motor BackEMF Vector Meas.                    
                        MCBaseAdress +  8: "VR1",   #15 & 1.65 Volt. Rail Meas.                    
                        MCBaseAdress +  9: "VR2",   #2.5 & 1.2 Volt. Rail Meas.                    
                        MCBaseAdress + 10: "FSM",   #Fan Speed Measurement
                        MCBaseAdress + 11: "SKT",   #Sink & Motor Temp. Meas.
                        MCBaseAdress + 12: "ICT",   #Air In & CPU Temp. Meas.
                        MCBaseAdress + 13: "OCT",   #Air out & Cap Temp. Meas.
                        MCBaseAdress + 14: "ODO"    #Odo. & Bus AmpHours Meas.
                        }
        self.formats = {"ID": "u_int32 + char[4]",  #Identification information
                        "Stat": "3*u_int16"         #Status Information}
                        }                           #Else: 2 floats 
        
        
        self.serialNumber = 12345 #Not sure
        self.tritID = "TRIa"
        self.activeMotor = 0
        #Flags inidicating errors
        self.errors = {"15VUVL" :0, #A 15V rail under voltage lock out occurred
                       "Conf"   :0, #Config Read Error
                       "Watch"  :0, #Watchdog caused last reset
                       "Halls"  :0, #Bad motor position hall sequence
                       "DCBusOV":0, #DC Bus over voltage
                       "SoftOC" :0, #Software over current
                       "HardOC" :0  #Hardware over current
                       }
        #Flags indicate limiting control loop                
        self.limits = {"HeatS"  :0, #Heatink Temperature
                       "BusVL"  :0, #Bus Voltage Lower Limit
                       "BusVU"  :0, #Bus Voltage Upper Limit
                       "BusC"   :0, #Bus Current
                       "Velo"   :0, #Velocity
                       "MotorC" :0, #Motor Current
                       "PWM"    :0  #Bridge PWM
                       }                
        self.busCurrent       = 0
        self.busVoltage       = 0
        self.vehicleVelocity  = 0
        self.motorVelocity    = 0
        self.phaseACurrent    = 0
        self.phaseBCurrent    = 0
        self.vectVoltReal     = 0
        self.vectVoltImag     = 0
        self.vectCurrReal     = 0
        self.vectCurrImag     = 0
        self.backEMFReal      = 0   #0 by definition
        self.backEMFImag      = 0
        self.fifteenVsupply   = 0
        self.onesixfiveVsupply= 0
        self.twofiveVsupply   = 0
        self.onetwoVsupply    = 0
        self.fanSpeed         = 0
        self.fanDrive         = 0
        self.heatSinkTemp     = 0
        self.motorTemp        = 0
        self.airInletTemp     = 0
        self.processorTemp    = 0
        self.airOutletTemp    = 0
        self.capacitorTemp    = 0
        self.DCBusAmpHours    = 0
        self.Odometer         = 0
    def parseoldSQL(self,row):
        self.ID = row[0]
        self.time = row[1]
        self.msgType = self.types[row[2]]
        try:
            self.msgFormat = self.formats[self.msgType]
        except:
            self.msgFormat = "2*float32"
            
        if   self.msgFormat == "u_int32 + char[4]": #Identification information
            pass   #These Values should not change
            
        elif self.msgFormat == "3*u_int16":  #Status Information
            '''
            self.a = [0,0,0,0,0,0,0,0]
            self.b = [0,0,0,0,0,0,0,0]
            self.a,self.b,self.c,self.d = struct.unpack("x????????x????????hh", row[3]) #Awful hacky bit flags
            self.limits["HeatS"]   = bin(self.a)[0]         
            self.limits["BusVL"]   = bin(self.a)[1]
            self.limits["BusVU"]   = bin(self.a)[2]
            self.limits["BusC"]    = bin(self.a)[3]
            self.limits["Velo"]    = bin(self.a)[4]
            self.limits["MotorC"]  = bin(self.a)[5]
            self.limits["PWM"]     = bin(self.a)[6]
            
            
            self.errors["15VUVL"]  = bin(self.b)[-7]
            self.errors["Conf"]    = bin(self.b)[-6]
            self.errors["Watch"]   = bin(self.b)[-5]
            self.errors["Halls"]   = bin(self.b)[-4]
            self.errors["DCBusOV"] = bin(self.b)[-3]
            self.errors["SoftOC"]  = bin(self.b)[-2]
            self.errors["HardOC"]  = bin(self.b)[-1]
            
            self.activeMotor = self.c
            '''
            pass
        else:
            self.a,self.b = struct.unpack("ff", row[3])
            if   self.msgType =="Bus":              #Bus Measurement   
                self.busCurrent = self.b
                self.busVoltage = self.a
                
            elif self.msgType =="Vel":              #Velocity Measurement
                self.vehicleVelocity = self.b
                self.motorVelocity = self.a
                
            elif self.msgType =="PhC":              #Phase Current Measurement
                self.phaseACurrent = self.b
                self.phaseBCurrent = self.a
                
            elif self.msgType =="MVV":              #Motor Voltage Vector Meas.
                self.vectVoltReal  = self.b
                self.vectVoltImag  = self.a
                
            elif self.msgType =="MVC":              #Motor Current Vector Meas.                       
                self.vectCurrReal  = self.b
                self.vectCurrImag  = self.a
                
            elif self.msgType =="MBE":              #Motor BackEMF Vector Meas.                    
                self.backEMFReal   = self.b
                self.backEMFImag   = self.a
                
            elif self.msgType =="VR1":              #15 & 1.65 Volt. Rail Meas.                    
                self.fifteenVsupply= self.b
                self.onesixfiveVsupply=self.a                
                
            elif self.msgType =="VR2":              #2.5 & 1.2 Volt. Rail Meas.                    
                self.twofiveVsupply= self.b
                self.onetwoVsupply = self.a
                
            elif self.msgType =="FSM":              #Fan Speed Measurement
                self.fanSpeed      = self.b
                self.fanDrive      = self.a
                
            elif self.msgType =="SKT":              #Sink & Motor Temp. Meas.
                self.heatSinkTemp  = self.b
                self.motorTemp     = self.a
                
            elif self.msgType =="ICT":              #Air In & CPU Temp. Meas.
                self.airInletTemp  = self.b
                self.processorTemp = self.a
                
            elif self.msgType =="OCT":              #Air out & Cap Temp. Meas.
                self.airOutletTemp = self.b
                self.capacitorTemp = self.a
                
            elif self.msgType =="ODO":              #Odo. & Bus AmpHours Meas.
                self.DCBusAmpHours = self.b
                self.Odometer      = self.a
        