from random import uniform, randint
import time

Population = []
Predators = []
Plane = 100
Predation = 1

for n in range(200):
    Rate = randint(10, 131071) # top number is a string of 17 '1's
    Gene = bin(Rate)
    Genome = Gene[2:].zfill(30) + ('0'*10)
    Genome += "10100" + ('0'*5) # oncogene 1 = 20 base 10
    Genome += "10100" + ('0'*5) # oncogene 2
    Genome += str(randint(0, Plane)).zfill(5) # x coord
    Genome += str(randint(0, Plane)).zfill(5) # y coord
    Population.append(Genome)

def mutate(Genome):
    Rate = int(Genome[13:30], 2)
    Prob = 1./Rate
    mutationZone = Genome[0:60]
    _ = ""
    for n in mutationZone:
        if Prob >= uniform(0, 1):
            _ += str(randint(0, 1))
        else:
            _ += n
    return _ + Genome[60:]

t0 = time.time()
for n in range(1000):
    map(mutate, Population)
t1 = time.time()
print((t1-t0)/1000)

# loops more efficient at scale
def mutateLoop(Population):
    _Pop = []
    for Genome in Population:
        Rate = int(Genome[13:30], 2)
        Prob = 1./Rate
        mutationZone = Genome[0:60]
        _ = ""
        for n in mutationZone:
            if Prob >= uniform(0, 1):
                _ += str(randint(0, 1))
            else:
                _ += n
        _Pop.append(_ + Genome[60:])
    return _Pop

t0 = time.time()
for n in range(1000):
    mutateLoop(Population)
t1 = time.time()
print((t1-t0)/1000)
