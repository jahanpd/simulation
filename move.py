from random import randint


def move_genome(List, Plane):
    _Pop = []
    for Organism in List:
        X = int(Organism[-19:-10])
        Y = int(Organism[-9:])
        NewX = randint(X-1, X+1)
        NewY = randint(Y-1, Y+1)
        if NewX not in range(Plane):
            NewX = X
        if NewY not in range(Plane):
            NewY = Y
        Genome = (Organism[0:200] + 'x' + str(NewX).zfill(9) + 'y' +
                                    str(NewY).zfill(9))
        _Pop.append(Genome)

    return _Pop


def move_predator(List, Plane):
    _Pop = []
    for Organism in List:
        X = int(Organism[-19:-10])
        Y = int(Organism[-9:])
        NewX = randint(X-1, X+1)
        NewY = randint(Y-1, Y+1)
        if NewX not in range(Plane):
            NewX = X
        if NewY not in range(Plane):
            NewY = Y
        Genome = ('x' + str(NewX).zfill(9) + 'y' + str(NewY).zfill(9))
        _Pop.append(Genome)

    return _Pop
