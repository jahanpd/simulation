<<<<<<< HEAD:predate.py
from random import uniform, randint
=======
from random import uniform
import time
import itertools
from backBone import generatePopulations
>>>>>>> ff2a79fa9ebad4634182885b7555d05d0524a412:Mapped/predate.py

Population, Predators = generatePopulations()

def predate(Population, Predators, Predation):
    _Pop = []
    Dead = []
    for Genome in Population:
        XY = Genome[-20:]
        if XY in Predators:
            if Predation < uniform(0, 1):
                _Pop.append(Genome)
            else:
                Dead.append(Genome)
        else:
            _Pop.append(Genome)
    return _Pop, Dead


<<<<<<< HEAD:predate.py
def predators(Population, Predators, Plane):
    Ratio = len(Population)/len(Predators)
    while len(Population)/len(Predators) > 2.5:
        Genome = ('x' + str(randint(0, Plane)).zfill(9) + 'y' +
                str(randint(0, Plane)).zfill(9))
        Predators.append(Genome)
    while len(Population)/len(Predators) < 2.5:
=======

def kill(Genome):
    location = Genome[:-10]
    return location not in Predators
>>>>>>> ff2a79fa9ebad4634182885b7555d05d0524a412:Mapped/predate.py
