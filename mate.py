from random import randint


def mate(Population, Plane):
    Daughters = []
    for Genome1 in Population:
        XY = Genome1[-20:]
        Index1 = Population.index(Genome1)
        for Genome2 in Population:
            Index2 = Population.index(Genome2)
            if Index1 != Index2:
                if XY in Genome2:
                    Rate1 = int(Genome1[0:100], 2)
                    Rate2 = int(Genome2[0:100], 2)
                    Newrate = (Rate1 + Rate2)/2
                    Gene = bin(Newrate)
                    Genome = Gene[2:].zfill(100) + ('0'*100)
                    Genome += 'x' + str(randint(0, Plane)).zfill(9)
                    Genome += 'y' + str(randint(0, Plane)).zfill(9)
                    Daughters.append(Genome)
    _Pop = Population + Daughters
    return _Pop
