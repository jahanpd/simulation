from random import uniform, randint
from mate import mate
from move import move_genome, move_predator
from predate import predate

Population = []
Predators = []
Plane = 100
Predation = 1

for n in range(2):
    Rate = randint(10, 131071) # top number is a string of 17 '1's
    Gene = bin(Rate)
    Genome = Gene[2:].zfill(30) + ('0'*10)
    Genome += "10100" + ('0'*5) # oncogene 1 = 20 base 10 (40-50)
    Genome += "10100" + ('0'*5) # oncogene 2 (50-60)
    Genome += str(randint(0, Plane)).zfill(5) # x coord
    Genome += str(randint(0, Plane)).zfill(5) # y coord
    Population.append(Genome)

for n in range(10):
    predatorLocation = str(randint(0, Plane)).zfill(5) + \
        str(randint(0, Plane)).zfill(5)
    Predators.append(predatorLocation)
