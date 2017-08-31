from random import uniform, randint
import numpy as np
import time
import matplotlib.pyplot as plt

Plane = 2
# use 1.03 instead for a much harsher pred population curve
def exponential(x):
    return int(np.power(1.015, x) + 1)

def population(popSize, Plane):
    rateGene1 = np.random.randint(1,high=1024, size=(popSize,1))
    rateGene2 = np.random.randint(1,high=1024, size=(popSize,1))
    oncogenes = np.full((popSize,3),20,dtype=np.int)
    location = np.random.randint(Plane+1,size=(popSize,2))
    generation = np.zeros((popSize,1), dtype=np.int)
    genomes = np.concatenate((rateGene1,rateGene2,oncogenes,generation,location),axis=1)
    predators = np.random.randint(Plane+1,size=((exponential(popSize)),2))
    return genomes, predators

def convertString(gene):
    string = bin(gene)
    return string[2:]

def convertInt(gene):
    if gene == "":
        return 1
    else:
        return int(gene, 2)

def geneSwitch(gene, rate):
    localRate = rate
    if localRate == 0:
        localRate += 1
    oncogenes = gene[0].zfill(5) + gene[1].zfill(5) + gene[2].zfill(5)
    Prob = 1./localRate
    mutate = ""
    for n in oncogenes:
        mutate += probabality(Prob, str(randint(0,1)), n)
    gene[0] = mutate[:5]
    gene[1] = mutate[5:10]
    gene[2] = mutate[10:]

def probabality(Prob, ifReturn, elReturn):
    if Prob >= uniform(0, 1):
        return ifReturn
    else:
        return elReturn

def mutate(genomes):
    rates = meanRates(genomes[:,0:2])
    oncogenes = genomes[:,2:5]
    stringConvert = np.vectorize(convertString)
    out = stringConvert(oncogenes)
    map(geneSwitch,out,rates)
    intConvert = np.vectorize(convertInt)
    genomes[:,2:5] = intConvert(out)

def meanRates(rates):
    meanrates = np.array([],dtype=int)
    for rate in rates:
        meanrates = np.append(meanrates, int(np.mean(rate)))
    return meanrates

def shift(coord, Prob):
    newCoord = probabality(Prob, randint(coord-1,coord+1), coord)
    if newCoord not in range(Plane):
        return Plane-1
    else:
        return newCoord

def move(genomes,moveProb):
    XY = genomes[:,-2:]
    Prob = 1./moveProb
    newCoordinate = np.vectorize(shift)
    genomes[:,-2:] = (newCoordinate(XY,Prob))

def inheritance(rate1a, rate1b, rate2a, rate2b):
    randprob = uniform(0, 1)
    if 0.25 >= randprob:
        return rate1a, rate2a
    elif 0.5 >= randprob:
        return rate1a, rate2b
    elif 0.75 >= randprob:
        return rate1b, rate2a
    elif 1 >= randprob:
        return rate1b, rate2b

def daughter(genome1, genome2, newRate1, newRate2):
    maxGen = np.amax(np.array([genome1[5],genome2[5]]))
    return np.array([newRate1,newRate2,20,20,20,maxGen+1,randint(0, Plane),randint(0, Plane)])

def sex(genome1, genome2):
    a = genome1[-2:]
    b = genome2[-2:]
    if (a==b).all():
        og1 = genome1[2:5]
        og2 = genome2[2:5]
        oncogeneCount = np.count_nonzero(og1==20) + np.count_nonzero(og2==20)
        if oncogeneCount == 2:
            fertility = 1
            newRate1, newRate2 = inheritance(genome1[0], genome1[1], genome2[0], genome2[1])
            return daughter(genome1, genome2, newRate1, newRate2)
        elif oncogeneCount == 3:
            fertility = 3
            progArray = np.empty([3,8], dtype=np.int)
            for n in range(fertility):
                newRate1, newRate2 = inheritance(genome1[0], genome1[1], genome2[0], genome2[1])
                progeny = daughter(genome1, genome2, newRate1, newRate2)
                progArray[n] = progeny
            return progArray
        else:
            return []
    else:
        return []

def mate(genomes):
    daughterArray = np.zeros([1,8], dtype=np.int)
    for i in range(len(genomes)):
        for j in range(i+1, len(genomes)):
            progeny = sex(genomes[i],genomes[j])
            if len(progeny) != 0:
                daughterArray = np.vstack([daughterArray, progeny])
    if len(daughterArray)>1:
        return daughterArray[1:,:]

def procreate(genomes, children):
    if children != None:
        return np.vstack([genomes, children])
    else:
        return genomes

a, b = population(5, Plane)
print a
for x in range(100):
    mutate(a)
    child = mate(a)
    print(child)
    a = procreate(a, child)
print a
