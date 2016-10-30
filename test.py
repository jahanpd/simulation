from random import uniform, randint
from mate import mate
from move import move

Population = []
Plane = 100

for n in range(20):
    Rate = randint(1000, 100000)
    Gene = bin(Rate)
    Genome = Gene[2:].zfill(100) + ('0'*100)
    Genome += 'x' + str(randint(0, Plane)).zfill(9)
    Genome += 'y' + str(randint(0, Plane)).zfill(9)
    Population.append(Genome)


print Population

# for Test in range(2):
while len(Population) != 0:
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
    Population = move(Population, Plane)
    print len(Population)
