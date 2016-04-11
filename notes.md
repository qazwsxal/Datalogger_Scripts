TODO:
=====

Elif in the room:
-----------------

Rewrite can parsing, using aliasing so we don't have a massive elif.
i.e.:
```
self._cangroups ={ "Vel" : (0,0)}
self.status = {"vehicleVelocity" : self.cangroups["Vel"][0],
               "motorVelocity"   : self.cangroups["Vel"][1]}


>>> self.status["vehicleVelocity"]
    0
>>> self._cangroups["Vel"][0] = 4  #obvously can;t usually write this

>>> self.status["vehicleVelocity"]
    4
```

