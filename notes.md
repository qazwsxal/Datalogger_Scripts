TODO:
=====

Using a dict as kwargs
----------------------
If we've got a load of kwargs to pass, we can pass them as a dict, this is especially useful when a method returns a dict:

Example:
```
>>> Wavesculptor20.status()
{'vectVoltImag': 0,
 'fanSpeed': 0,
 'airOutletTemp': 0,
 'backEMFImag': 0,
 'onesixfiveVsupply': 0,
 'vectCurrImag': 0,
 'Odometer': 0,
 'phaseBCurrent': 0,
 'processorTemp': 0,
 'fanDrive': 0,
 'busVoltage': 0,
 'fifteenVsupply': 0,
 'vectVoltReal': 0,
 'airInletTemp': 0,
 'heatSinkTemp': 0,
 'backEMFReal': 0,
 'capacitorTemp': 0,
 'motorTemp': 0,
 'twofiveVsupply': 0,
 'vectCurrReal': 0,
 'vehicleVelocity': 0,
 'phaseACurrent': 0,
 'motorVelocity': 0,
 'onetwoVsupply': 0,
 'DCBusAmpHours': 0,
 'busCurrent': 0}
```
If we then want to put this into a line in the sql db we can call something like this:

```
session.add(motorORM(**Wavesculptor20.status()))
session.commit()
```
