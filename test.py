from random import randint
from run import run

Population = []
Predators = []
Food = []
Plane = 100
Predation = 1

for n in range(100):
    Rate = randint(1000, 10000)
    Gene = bin(Rate)
    Genome = Gene[2:].zfill(100) + ('0'*100)
    Genome += 'x' + str(randint(0, Plane)).zfill(9)
    Genome += 'y' + str(randint(0, Plane)).zfill(9)
    Population.append(Genome)

for n in range(50):
    Genome = ('x' + str(randint(0, Plane)).zfill(9) + 'y' +
            str(randint(0, Plane)).zfill(9))
    Predators.append(Genome)

for n in range(50):
    Location = ('x' + str(randint(0, Plane)).zfill(9) + 'y' +
            str(randint(0, Plane)).zfill(9))
    Food.append(Location)

run(Population, Predators, Plane, Predation)
