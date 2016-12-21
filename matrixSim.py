from random import uniform, randint
import numpy as np
import time
import matplotlib.pyplot as plt

def exponential(x):
    return int(np.power(1.025, x) + 1)

def population(popSize, Plane):
    rateGene = np.random.randint(1,high=1024, size=(popSize,1))
    oncogenes = np.full((popSize,3),20,dtype=np.int)
    location = np.random.randint(Plane+1,size=(popSize,2))
    generation = np.zeros((popSize,1), dtype=np.int)
    genomes = np.concatenate((rateGene,oncogenes,generation,location),axis=1)
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

def probabality(Prob, ifReturn, elReturn):
    if Prob >= uniform(0, 1):
        return ifReturn
    else:
        return elReturn

def geneSwitch(gene, rate):
    oncogenes = gene[0] + gene[1] + gene[2]
    Prob = 1./rate
    mutate = ""
    for n in oncogenes:
        mutate += probabality(Prob, str(randint(0,1)), n)
    gene[0] = mutate[:5]
    gene[1] = mutate[5:10]
    gene[2] = mutate[10:]

def mutate(genomes):
    rates = genomes[:,0]
    oncogenes = genomes[:,1:4]
    stringConvert = np.vectorize(convertString)
    out = stringConvert(oncogenes)
    map(geneSwitch,out,rates)
    intConvert = np.vectorize(convertInt)
    genomes[:,1:4] = intConvert(out)

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

def checkLength(rate):
    if len(rate)<10:
        return rate.zfill(10)
    else:
        return rate

def inheritance(rate1, rate2):
    rate1 = checkLength(convertString(rate1))
    rate2 = checkLength(convertString(rate2))
    newRate1 = convertInt(rate1[:5] + rate2[5:])
    newRate2 = convertInt(rate2[:5] + rate1[5:])
    return probabality(0.5, newRate1, newRate2)


def daughter(genome1, genome2, newRate):
    maxGen = np.amax(np.array([genome1[4],genome2[4]]))
    return np.array([newRate,20,20,20,maxGen+1,randint(0, Plane),randint(0, Plane)])

def sex(genome1, genome2):
    a = genome1[-2:]
    b = genome2[-2:]
    if (a==b).all():
        og1 = genome1[1:4]
        og2 = genome2[1:4]
        oncogeneCount = np.count_nonzero(og1==20) + np.count_nonzero(og2==20)
        if oncogeneCount == 2:
            fertility = 1
            newRate = inheritance(genome1[0],genome2[0])
            return daughter(genome1, genome2, newRate)
        elif oncogeneCount == 3:
            fertility = 3
            progArray = np.empty([3,7], dtype=np.int)
            for n in range(fertility):
                newRate = inheritance(genome1[0],genome2[0])
                progeny = daughter(genome1, genome2, newRate)
                progArray[n] = progeny
            return progArray
        else:
            return []
    else:
        return []

def mate(genomes):
    daughterArray = np.zeros([1,7], dtype=np.int)
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

def cancer(genome):
    oncogenes = genome[1:4]
    oncogeneCount=np.count_nonzero(oncogenes==20)
    if oncogeneCount==0:
        return False
    else:
        return True

def kill(genome):
    location = genome[-2:]
    if location.tolist() in predators.tolist():
        oncogenes = genome[1:4]
        oncogeneCount=np.count_nonzero(oncogenes==20)
        if oncogeneCount == 2:
            Prob = predationRate
        else:
            Prob = predationRate*3
        return probabality(Prob, False, True)
    else:
        return True

def predatorEndangered(predators, predSize):
    _Predators = predators
    while len(_Predators) < predSize:
        newp = np.random.randint(Plane+1,size=(1,2))
        _Predators = np.vstack([_Predators, newp])
    return _Predators

def predatorLevels(predators):
    predSize = exponential(len(genomes))
    if len(predators) > predSize:
        return predators[0:predSize]
    elif len(predators) < predSize:
        muchosPred = predatorEndangered(predators, predSize)
        return muchosPred
    else:
        return predators

def popMax(genomes, popMax):
    if len(genomes) > popMax:
        select = np.random.randint(len(genomes), size=popMax)
        return genomes[select,:]
    else:
        return genomes


# predator population controlled by exp function y = a(b^x)+c where
# a = 1
# b = 1.025
# c = 1


iters = 10000
popCap = 200

rateAvg1 = []
populSize1 = []
organismMoveRate = 1
predationRate = 0.8
genomes, predators = population(100,50)

for n in range(iters):
    t0 = time.time()
    Plane = 50
    mutate(genomes)
    move(genomes,organismMoveRate)
    move(predators, 1)
    predators = predatorLevels(predators)
    child = mate(genomes)
    genomes = procreate(genomes, child)
    genomes = np.array(filter(cancer, genomes))
    genomes = np.array(filter(kill, genomes))
    genomes = popMax(genomes, popCap)
    if len(genomes) <= 1:
        break
    rateAvg1.append(np.mean(genomes[:,0]))
    populSize1.append(len(genomes))
    t1 = time.time()
    print(n,t1-t0, Plane, len(genomes), len(predators))

spread1 = 0
if len(genomes) > 1:
    spread1 = [np.min(genomes[:,0]),np.max(genomes[:,0])]

organismMoveRate = 1
predationRate = 0.4
genomes, predators = population(100,50)
rateAvg2 = []
populSize2 = []

for n in range(iters):
    t0 = time.time()
    Plane = 50
    mutate(genomes)
    move(genomes,organismMoveRate)
    move(predators, 1)
    predators = predatorLevels(predators)
    child = mate(genomes)
    genomes = procreate(genomes, child)
    genomes = np.array(filter(cancer, genomes))
    genomes = np.array(filter(kill, genomes))
    genomes = popMax(genomes, popCap)
    if len(genomes) <= 1:
        break
    rateAvg2.append(np.mean(genomes[:,0]))
    populSize2.append(len(genomes))
    t1 = time.time()
    print(n,t1-t0, Plane, len(genomes),len(predators))

spread2 = 0
if len(genomes) > 1:
    spread2 = [np.min(genomes[:,0]),np.max(genomes[:,0])]

print(rateAvg1[len(rateAvg1)-1],spread1)

print(rateAvg2[len(rateAvg2)-1],spread2)

plt.plot(
        range(len(rateAvg1)),rateAvg1,'g-',\
        range(len(rateAvg2)), rateAvg2,'r-', \
        range(len(populSize1)), populSize1,'g-',\
        range(len(populSize2)), populSize2,'r-')
plt.show()
