from random import uniform, randint
from mate import mate
from move import move_genome, move_predator
from predate import predate


def run(Population, Predators, Plane, Predation):
    Dead = []
    while len(Population) < 100:
        _Pop = []
        for Genome in Population:
            Rate = int(Genome[0:100], 2)
            Prob = 1./Rate
            _ = ""
            for n in Genome:
                if Prob >= uniform(0, 1):
                    _ += str(randint(0, 1))
                else:
                    _ += n
            Genome = _
            Newrate = int(Genome[0:100], 2)
            if Rate == Newrate:
                _Pop.append(Genome)

        Population = _Pop

        Population = mate(Population, Plane)
        Population, X, Y = move_genome(Population, Plane)
        Predators = move_predator(Predators, Plane)
        Population, Died = predate(Population, Predators, Predation)
        Dead = Dead + Died
        print len(Population)
        print len(Dead)
        _X = open('X.txt', 'w')
        for In in X:
            _X.write("%s\n" % In)
        _Y = open('Y.txt', 'w')
        for In in Y:
            _Y.write("%s\n" % In)
