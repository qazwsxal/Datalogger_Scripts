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
    busCurrent = sqla.Column(sqla.Float)
    busVoltage = sqla.Column(sqla.Float)
    vehicleVelocity = sqla.Column(sqla.Float)
    motorVelocity = sqla.Column(sqla.Float)
    phaseACurrent = sqla.Column(sqla.Float)
    phaseBCurrent = sqla.Column(sqla.Float)
    vectVoltReal = sqla.Column(sqla.Float)
    vectVoltImag = sqla.Column(sqla.Float)
    vectCurrReal = sqla.Column(sqla.Float)
    vectCurrImag = sqla.Column(sqla.Float)
    backEMFReal = sqla.Column(sqla.Float)
    backEMFImag = sqla.Column(sqla.Float)
    fifteenVsupply = sqla.Column(sqla.Float)
    onesixfiveVsupply = sqla.Column(sqla.Float)
    twofiveVsupply = sqla.Column(sqla.Float)
    onetwoVsupply = sqla.Column(sqla.Float)
    fanSpeed = sqla.Column(sqla.Float)
    fanDrive = sqla.Column(sqla.Float)
    heatSinkTemp = sqla.Column(sqla.Float)
    motorTemp = sqla.Column(sqla.Float)
    airInletTemp = sqla.Column(sqla.Float)
    processorTemp = sqla.Column(sqla.Float)
    airOutletTemp = sqla.Column(sqla.Float)
    capacitorTemp = sqla.Column(sqla.Float)
    DCBusAmpHours = sqla.Column(sqla.Float)
    Odometer = sqla.Column(sqla.Float)

    def __repr__(self):
        return "<WS20_ORM(busCurrent='%s', busVoltage='%s', \
                vehicleVelocity='%s')>" % (
                self.busCurrent, self.busVoltage, self.vehicleVelocity)


class Controls_ORM(Base):
    __tablename__ = 'controls'

    msg_id = sqla.Column(sqla.BigInteger, primary_key=True)
    time = sqla.Column(DATETIME(fsp=4))
    busCurrent = sqla.Column(sqla.Float)
    motorCurrent = sqla.Column(sqla.Float)
    motorVelocity = sqla.Column(sqla.Float)


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
