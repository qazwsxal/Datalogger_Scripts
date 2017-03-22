import sqlalchemy as sqla
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import DATETIME
Base = declarative_base()


class WS20_ORM(Base):
    ''' Object-Relational Map for Wavesculptor 20
    '''
    __tablename__ = 'motorstate'

    msg_id = sqla.Column(sqla.BigInteger, primary_key=True)
    time = sqla.Column(DATETIME(fsp=4))
    busCurrent = sqla.Column(sqla.Float, server_default=None, nullable=True)
    busVoltage = sqla.Column(sqla.Float, server_default=None, nullable=True)
    vehicleVelocity = sqla.Column(sqla.Float, server_default=None, nullable=True)
    motorVelocity = sqla.Column(sqla.Float, server_default=None, nullable=True)
    phaseACurrent = sqla.Column(sqla.Float, server_default=None, nullable=True)
    phaseBCurrent = sqla.Column(sqla.Float, server_default=None, nullable=True)
    vectVoltReal = sqla.Column(sqla.Float, server_default=None, nullable=True)
    vectVoltImag = sqla.Column(sqla.Float, server_default=None, nullable=True)
    vectCurrReal = sqla.Column(sqla.Float, server_default=None, nullable=True)
    vectCurrImag = sqla.Column(sqla.Float, server_default=None, nullable=True)
    backEMFReal = sqla.Column(sqla.Float, server_default=None, nullable=True)
    backEMFImag = sqla.Column(sqla.Float, server_default=None, nullable=True)
    fifteenVsupply = sqla.Column(sqla.Float, server_default=None, nullable=True)
    onesixfiveVsupply = sqla.Column(sqla.Float, server_default=None, nullable=True)
    twofiveVsupply = sqla.Column(sqla.Float, server_default=None, nullable=True)
    onetwoVsupply = sqla.Column(sqla.Float, server_default=None, nullable=True)
    fanSpeed = sqla.Column(sqla.Float, server_default=None, nullable=True)
    fanDrive = sqla.Column(sqla.Float, server_default=None, nullable=True)
    heatSinkTemp = sqla.Column(sqla.Float, server_default=None, nullable=True)
    motorTemp = sqla.Column(sqla.Float, server_default=None, nullable=True)
    airInletTemp = sqla.Column(sqla.Float, server_default=None, nullable=True)
    processorTemp = sqla.Column(sqla.Float, server_default=None, nullable=True)
    airOutletTemp = sqla.Column(sqla.Float, server_default=None, nullable=True)
    capacitorTemp = sqla.Column(sqla.Float, server_default=None, nullable=True)
    DCBusAmpHours = sqla.Column(sqla.Float, server_default=None, nullable=True)
    Odometer = sqla.Column(sqla.Float, server_default=None, nullable=True)

    def __repr__(self):
        return "<WS20_ORM(busCurrent='%s', busVoltage='%s', \
                vehicleVelocity='%s')>" % (
                self.busCurrent, self.busVoltage, self.vehicleVelocity)


class Controls_ORM(Base):
    __tablename__ = 'controls'

    msg_id = sqla.Column(sqla.BigInteger, primary_key=True)
    time = sqla.Column(DATETIME(fsp=4))
    setBusCurrent = sqla.Column(sqla.Float, server_default=None, nullable=True)
    setMotorCurrent = sqla.Column(sqla.Float, server_default=None, nullable=True)
    setMotorVelocity = sqla.Column(sqla.Float, server_default=None, nullable=True)

class BMS_ORM(Base):
    __tablename__ = 'batteries'

    msg_id = sqla.Column(sqla.BigInteger, primary_key=True)
    time = sqla.Column(DATETIME(fsp=4))
    modID = sqla.Column(sqla.Integer)
    cycles = sqla.Column(sqla.Integer)
    OTP = sqla.Column(sqla.Integer)
    OVP = sqla.Column(sqla.Integer)
    LVP = sqla.Column(sqla.Integer)
    cellV0 = sqla.Column(sqla.Float)
    cellV1 = sqla.Column(sqla.Float)
    cellV2 = sqla.Column(sqla.Float)
    cellV3 = sqla.Column(sqla.Float)

class GPS_ORM(Base):
    __tablename__ = 'gps_tpv'

    msg_id = sqla.Column(sqla.BigInteger, primary_key=True)
    device = sqla.Column(sqla.String(13))
    tag = sqla.Column(sqla.String(40))
    mode = sqla.Column(sqla.SmallInteger)
    time = sqla.Column(DATETIME(fsp=4))
    ept = sqla.Column(sqla.Float) 
    lat = sqla.Column(sqla.Float) 
    lon = sqla.Column(sqla.Float) 
    alt = sqla.Column(sqla.Float) 
    epx = sqla.Column(sqla.Float) 
    epy = sqla.Column(sqla.Float) 
    epv = sqla.Column(sqla.Float) 
    track = sqla.Column(sqla.Float) 
    speed = sqla.Column(sqla.Float) 
    climb = sqla.Column(sqla.Float) 
    epd = sqla.Column(sqla.Float) 
    eps = sqla.Column(sqla.Float) 
    epc = sqla.Column(sqla.Float)
