from random import uniform, randint


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


def predators(Population, Predators, Plane):
    Ratio = len(Population)/len(Predators)
    while len(Population)/len(Predators) > 2.5:
        Genome = ('x' + str(randint(0, Plane)).zfill(9) + 'y' +
                str(randint(0, Plane)).zfill(9))
        Predators.append(Genome)
    while len(Population)/len(Predators) < 2.5:
