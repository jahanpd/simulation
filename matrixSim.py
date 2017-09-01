from random import uniform, randint
import numpy as np
import time
import matplotlib.pyplot as plt

# use 1.03 instead for a much harsher pred population curve


def exponential(predCurve, x):
    return int(np.power(predCurve, x) + 1)


def population(popSize, Plane, predCurve):
    rateGene1 = np.random.randint(1, high=300, size=(popSize, 1))
    rateGene2 = np.random.randint(1, high=300, size=(popSize, 1))
    oncogenes = np.full((popSize, 3), 20, dtype=np.int)
    location = np.random.randint(Plane+1, size=(popSize, 2))
    generation = np.zeros((popSize, 1), dtype=np.int)
    genomes = np.concatenate((rateGene1, rateGene2, oncogenes, generation,
                             location), axis=1)
    predators = np.random.randint(Plane+1, size=((exponential(predCurve,
                                                              popSize)), 2))
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
    localRate = rate
    if localRate == 0:
        localRate += 1
    oncogenes = gene[0].zfill(5) + gene[1].zfill(5) + gene[2].zfill(5)
    Prob = 1./localRate
    mutate = ""
    for n in oncogenes:
        mutate += probabality(Prob, str(randint(0, 1)), n)
    gene[0] = mutate[:5]
    gene[1] = mutate[5:10]
    gene[2] = mutate[10:]


def meanRates(rates):
    meanrates = np.array([], dtype=int)
    for rate in rates:
        meanrates = np.append(meanrates, int(np.mean(rate)))
    return meanrates


def mutate(genomes):
    rates = meanRates(genomes[:, 0:2])
    oncogenes = genomes[:, 2:5]
    stringConvert = np.vectorize(convertString)
    out = stringConvert(oncogenes)
    map(geneSwitch, out, rates)
    intConvert = np.vectorize(convertInt)
    genomes[:, 2:5] = intConvert(out)


def shift(coord, Prob):
    newCoord = probabality(Prob, randint(coord-1, coord+1), coord)
    if newCoord not in range(Plane):
        return Plane-1
    else:
        return newCoord


def move(genomes, moveProb):
    XY = genomes[:, -2:]
    Prob = 1./moveProb
    newCoordinate = np.vectorize(shift)
    genomes[:, -2:] = (newCoordinate(XY, Prob))


def checkLength(rate):
    if len(rate) < 10:
        return rate.zfill(10)
    else:
        return rate


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
    maxGen = np.amax(np.array([genome1[5], genome2[5]]))
    return np.array([newRate1, newRate2, 20, 20, 20, maxGen+1,
                     randint(0, Plane), randint(0, Plane)])


def sex(genome1, genome2):
    a = genome1[-2:]
    b = genome2[-2:]
    if (a == b).all():
        og1 = genome1[2:5]
        og2 = genome2[2:5]
        oncogeneCount = np.count_nonzero(og1 == 20) + np.count_nonzero(og2 ==
                                                                       20)
        if oncogeneCount == 2:
            fertility = 1
            newRate1, newRate2 = inheritance(genome1[0], genome1[1],
                                             genome2[0], genome2[1])
            return daughter(genome1, genome2, newRate1, newRate2)
        elif oncogeneCount == 3:
            fertility = 3
            progArray = np.empty([3, 8], dtype=np.int)
            for n in range(fertility):
                newRate1, newRate2 = inheritance(genome1[0], genome1[1],
                                                 genome2[0], genome2[1])
                progeny = daughter(genome1, genome2, newRate1, newRate2)
                progArray[n] = progeny
            return progArray
        else:
            return []
    else:
        return []


def mate(genomes):
    daughterArray = np.zeros([1, 8], dtype=np.int)
    for i in range(len(genomes)):
        for j in range(i+1, len(genomes)):
            progeny = sex(genomes[i], genomes[j])
            if len(progeny) != 0:
                daughterArray = np.vstack([daughterArray, progeny])
    if len(daughterArray) > 1:
        return daughterArray[1:, :]


def procreate(genomes, children):
    if children is not None:
        return np.vstack([genomes, children])
    else:
        return genomes


def cancer(genome):
    oncogenes = genome[2:5]
    oncogeneCount = np.count_nonzero(oncogenes == 20)
    if oncogeneCount == 0:
        return False
    else:
        return True


def kill1(genome):
    location = genome[-2:]
    if location.tolist() in predators1.tolist():
        oncogenes = genome[2:5]
        oncogeneCount = np.count_nonzero(oncogenes == 20)
        if oncogeneCount == 2:
            Prob = predationRate1
        else:
            Prob = predationRate1*3
        return Prob <= uniform(0, 1)
    else:
        return True


def kill2(genome):
    location = genome[-2:]
    if location.tolist() in predators2.tolist():
        oncogenes = genome[2:5]
        oncogeneCount = np.count_nonzero(oncogenes == 20)
        if oncogeneCount == 2:
            Prob = predationRate2
        else:
            Prob = predationRate2*3
        return Prob <= uniform(0, 1)
    else:
        return True


def predatorEndangered(predators, predSize):
    _Predators = predators
    while len(_Predators) < predSize:
        newp = np.random.randint(Plane+1, size=(1, 2))
        _Predators = np.vstack([_Predators, newp])
    return _Predators


def predatorLevels(genomes, predators, predCurve):
    predSize = exponential(predCurve, len(genomes))
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
        return genomes[select, :]
    else:
        return genomes


def diversity(genomes, Plane, predCurve):
    replaceNum = int(0.03*len(genomes))
    for n in np.random.randint(0, high=len(genomes), size=replaceNum):
        genomes[n], discard = population(1, Plane, predCurve)


# predator population controlled by exp function y = a(b^x)+c where
# a = 1
# b = 1.025
# c = 1

iterations = input("how many cycles of the simulation?? ")

stats = []
for run in range(iterations):
    iters = 3000
    popCap = 1000
    rateAvg1 = []
    populSize1 = []
    rateStd1 = []
    organismMoveRate1 = 1
    predCurve1 = 1.035  # larger number is harsher
    predationRate1 = 1
    genomes1, predators1 = population(100, 50, predCurve1)

    for n in range(iters):
        t0 = time.time()
        Plane = int(0.5*len(genomes1))
        mutate(genomes1)
        move(genomes1, organismMoveRate1)
        move(predators1, organismMoveRate1)
        predators1 = predatorLevels(genomes1, predators1, predCurve1)
        child = mate(genomes1)
        genomes1 = procreate(genomes1, child)
        genomes1 = np.array(filter(cancer, genomes1))
        genomes1 = np.array(filter(kill1, genomes1))
        genomes1 = popMax(genomes1, popCap)
        if n % 100 == 0:
            diversity(genomes1, Plane, predCurve1)
        if len(genomes1) <= 1:
            break
        ratesAll = meanRates(genomes1[:, 0:2])
        rateAvg1.append(np.mean(ratesAll))
        rateStd1.append(np.std(ratesAll))
        populSize1.append(len(genomes1))
        if np.std(ratesAll) == 0:
            break
        t1 = time.time()
        print(run, n, t1-t0, int(np.mean(ratesAll)), int(np.std(ratesAll)),
              len(genomes1), len(predators1), np.max(genomes1[:, 5]))

    spread1 = 0
    if len(genomes1) > 1:
        spread1 = [np.min(ratesAll), np.max(ratesAll)]

    organismMoveRate2 = 1
    predationRate2 = 0.3
    predCurve2 = 1.025  # larger predCurves mean harsher predation curves
    genomes2, predators2 = population(100, 50, predCurve2)
    rateAvg2 = []
    populSize2 = []
    rateStd2 = []

    for n in range(iters):
        t0 = time.time()
        Plane = int(0.5*len(genomes2))
        mutate(genomes2)
        move(genomes2, organismMoveRate2)
        move(predators2, 1)
        predators2 = predatorLevels(genomes2, predators2, predCurve2)
        child = mate(genomes2)
        genomes2 = procreate(genomes2, child)
        genomes2 = np.array(filter(cancer, genomes2))
        genomes2 = np.array(filter(kill2, genomes2))
        genomes2 = popMax(genomes2, popCap)
        if n % 100 == 0:
            diversity(genomes2, Plane, predCurve2)
        if len(genomes2) <= 1:
            break
        ratesAll = meanRates(genomes2[:, 0:2])
        rateAvg2.append(np.mean(ratesAll))
        rateStd2.append(np.std(ratesAll))
        populSize2.append(len(genomes2))
        if np.std(ratesAll) == 0:
            break
        t1 = time.time()
        print(run, n, t1-t0, int(np.mean(ratesAll)), int(np.std(ratesAll)),
              len(genomes2), len(predators2), np.max(genomes2[:, 5]))

    spread2 = 0
    if len(genomes2) > 1:
        spread2 = [np.min(ratesAll), np.max(ratesAll)]

    stats.append(rateAvg1[len(rateAvg1)-1])
    stats.append(spread1)

    stats.append(rateAvg2[len(rateAvg2)-1])
    stats.append(spread2)

    highPred = plt.plot(range(len(rateAvg1)), rateAvg1, 'g-', label='high')
    lowPred = plt.plot(range(len(rateAvg2)), rateAvg2, 'r-', label='low')
    popHigh = plt.plot(range(len(populSize1)), populSize1, 'g-')
    popLow = plt.plot(range(len(populSize2)), populSize2, 'r-')

    rateAvg1 = np.array(rateAvg1)
    rateStd1 = np.array(rateStd1)
    rateAvg2 = np.array(rateAvg2)
    rateStd2 = np.array(rateStd2)
    plt.fill_between(range(len(rateAvg1)), rateAvg1+rateStd1,
                     rateAvg1-rateStd1)
    plt.fill_between(range(len(rateAvg2)), rateAvg2+rateStd2,
                     rateAvg2-rateStd2)
    fig1 = plt.gcf()
    filename = "plot%s.png" % run
    fig1.savefig(filename)
    plt.close()

statsExport = open('stats.txt', 'w')
for n in stats:
    statsExport.write("%s," % n)
statsExport.close()
