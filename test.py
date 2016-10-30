from random import uniform, randint

Population = []

for n in range(100):
    Rate = randint(1000, 100000)
    Gene = bin(Rate)
    Genome = Gene[2:].zfill(100) + ('0'*100)
    Population.append(Genome)

while len(Population) != 0:
    _Pop = []
    Dead = []
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
    print len(Population)
