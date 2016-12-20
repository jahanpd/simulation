from random import uniform, randint
import itertools

# Global variables
Plane = 5
Predation = 0.005 # ratio of predators to population
populationSize = 20
populationCap = 200
maxGeneration = 200 # global max for generations of simulation

def move(organism):
    X = int(organism[-10:-5])
    Y = int(organism[-5:])
    NewX = randint(X-1, X+1)
    NewY = randint(Y-1, Y+1)
    if NewX not in range(Plane):
        NewX = X
    if NewY not in range(Plane):
        NewY = Y
    return organism[:-10] + str(NewX).zfill(5) + str(NewY).zfill(5)

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

def spawnGenome(rateGene, generation):
    Genome = rateGene[2:].zfill(30) + ('0'*10)
    Genome += "10100" + ('0'*5) # oncogene 1 = 20 base 10 (40-50)
    Genome += "10100" + ('0'*5) # oncogene 2 (50-60)
    Genome += (str(generation+1)).zfill(5) + ('0'*5) # generation tag
    Genome += str(randint(0, Plane)).zfill(5) # x coord
    Genome += str(randint(0, Plane)).zfill(5) # y coord
    return Genome


def generatePopulations():
    Population = []
    Predators = []
    for n in range(populationSize):
        Rate = randint(10, 131071) # top number is a string of 17 '1's
        Gene = bin(Rate)
        Genome = spawnGenome(Gene, 0)
        Population.append(Genome)

    for n in range(int(populationSize*Predation)):
        predatorLocation = str(randint(0, Plane)).zfill(5) + \
            str(randint(0, Plane)).zfill(5)
        Predators.append(predatorLocation)

    return Population, Predators

def kill(Genome):
    location = Genome[-10:]
    return location not in Predators

def cancer(Genome):
    oncogeneJuan = Genome[40:45]
    oncogeneDos = Genome[50:55]
    return oncogeneJuan=="10100" or oncogeneDos=="10100"

def mate(Population):
    Daughters = []
    for a, b in itertools.combinations(Population, 2):
        daughter = sex(a, b)
        if daughter != None:
            Daughters += daughter
    return Daughters

def XORfertility(onco1, onco2):
    if bool(onco1=="10100") ^ bool(onco2=="10100"):
        fertility = 3
    else:
        fertility = 1

def oncogeneFertility(genomeOne, genomeTwo):
    oncogeneJuanOne = genomeOne[40:45]
    oncogeneDosOne = genomeOne[50:55]
    oncogeneJuanTwo = genomeTwo[40:45]
    oncogeneDosTwo = genomeTwo[50:55]
    fertility1 = XORfertility(oncogeneJuanOne,oncogeneDosOne)
    fertility2 = XORfertility(oncogeneJuanTwo,oncogeneDosTwo)
    if fertility1 > fertility2:
        return fertility1
    else:
        return fertility2

def sex(genomeOne, genomeTwo):
    locationOne = genomeOne[-10:]
    locationTwo = genomeTwo[-10:]
    generationOne = int(genomeOne[-20:-15])
    generationTwo = int(genomeTwo[-20:-15])
    if locationOne == locationTwo:
        progeny = []
        fertility = oncogeneFertility(genomeOne,genomeTwo)
        for n in range(fertility):
            rateOne = int(genomeOne[13:30],2)
            rateTwo = int(genomeTwo[13:30],2)
            newRate = int(rateOne + rateTwo)/2
            newGene = bin(newRate)
            if generationOne > generationTwo:
                newGenome = spawnGenome(newGene, generationOne)
            else:
                newGenome = spawnGenome(newGene, generationTwo)
            progeny.append(newGenome)
        return progeny

def predatorEndangered(Predators):
    _Predators = Predators
    while len(_Predators) < 0.5*len(Population):
        predatorLocation = str(randint(0, Plane)).zfill(5) + \
            str(randint(0, Plane)).zfill(5)
        _Predators.append(predatorLocation)
    return _Predators

def predatorLevels(Predators):
    if len(Predators) > Predation*len(Population):
        return Predators[0:int(Predation*len(Population))]
    elif len(Predators) < Predation*len(Population):
        muchosPred = predatorEndangered(Predators)
        return muchosPred
    else:
        return Predators

Population, Predators = generatePopulations()

for n in range(10000):
    Population = map(move,Population)
    Predators = map(move,Predators)
    Population = mutateLoop(Population)
    Population = filter(kill, Population)
    Population = filter(cancer, Population)
    Daughters = mate(Population)
    Population = Population + Daughters
    Predators = predatorLevels(Predators)
    print(len(Population))
    print(len(Predators))
    if len(Population)==0:
        print(n)
        print(len(Predators))
        break
print(Predators)
