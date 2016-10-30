from random import uniform


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
