import sqlalchemy as sqla
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class WS20_DOM(Base):
    __tablename__ = 'motorstate'

    id = sqla.Column(sqla.BigInteger, primary_key=True)
    time = sqla.Column(sqla.DateTime)
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
        return "<WS20_DOM(busCurrent='%s', busVoltage='%s', vehicleVelocity='%s')>" % (
                self.busCurrent, self.busVoltage, self.vehicleVelocity)

