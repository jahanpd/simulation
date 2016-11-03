from random import randint
from plot import plot
from run import run
from threading import Thread

Population = []
Predators = []
Plane = 100
Predation = 1

for n in range(50):
    Rate = randint(1000, 100000)
    Gene = bin(Rate)
    Genome = Gene[2:].zfill(100) + ('0'*100)
    Genome += 'x' + str(randint(0, Plane)).zfill(9)
    Genome += 'y' + str(randint(0, Plane)).zfill(9)
    Population.append(Genome)

for n in range(50):
    Genome = ('x' + str(randint(0, Plane)).zfill(9) + 'y' +
            str(randint(0, Plane)).zfill(9))
    Predators.append(Genome)

print Predators

if __name__ == '__main__':
    Thread(target=run(Population, Predators, Plane, Predation)).start()
    Thread(target=plot(Population)).start()
