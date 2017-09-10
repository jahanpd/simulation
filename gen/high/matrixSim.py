from random import uniform, randint
import numpy as np
import time

# use 1.03 instead for a much harsher pred population curve


def exponential(predCurve, x):
    return int(np.power(predCurve, x) + 1)


def population(popSize, Plane, predCurve, High):
    rateGene1 = np.random.randint(1, high=High, size=(popSize, 1))
    rateGene2 = np.random.randint(1, high=High, size=(popSize, 1))
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


def probabality(Prob, ifReturn, elReturn, maxRate):
    if Prob <= randint(1, 0.8*maxRate):
        return ifReturn
    else:
        return elReturn


def meanRates(rates):
    meanrates = np.array([], dtype=int)
    for rate in rates:
        meanrates = np.append(meanrates, int(np.mean(rate)))
    return meanrates


def mutate(genomes, maxRate):
    rates = meanRates(genomes[:, 0:2])
    oncogenes = genomes[:, 2:5]
    stringConvert = np.vectorize(convertString)
    out = stringConvert(oncogenes)

    def geneSwitch(gene, rate):
        oncogenes = gene[0].zfill(5) + gene[1].zfill(5) + gene[2].zfill(5)
        Prob = float(rate)/maxRate
        mutate = ""
        for n in oncogenes:
            mutate += probabality(rate, str(randint(0, 1)), n, maxRate)
        gene[0] = mutate[:5]
        gene[1] = mutate[5:10]
        gene[2] = mutate[10:]

    map(geneSwitch, out, rates)
    intConvert = np.vectorize(convertInt)
    genomes[:, 2:5] = intConvert(out)


def probabalityMove(Prob, ifReturn, elReturn):
    if Prob >= uniform(0, 1):
        return ifReturn
    else:
        return elReturn


def shift(coord, Prob, Plane):
    newCoord = probabalityMove(Prob, randint(coord-1, coord+1), coord)
    if newCoord not in range(Plane):
        return Plane-1
    else:
        return newCoord


def move(genomes, moveProb, Plane):
    XY = genomes[:, -2:]
    Prob = 1./moveProb
    newCoordinate = np.vectorize(shift)
    genomes[:, -2:] = (newCoordinate(XY, Prob, Plane))


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


def daughter(genome1, genome2, newRate1, newRate2, Plane):
    maxGen = np.amax(np.array([genome1[5], genome2[5]]))
    return np.array([newRate1, newRate2, 20, 20, 20, maxGen+1,
                     randint(0, Plane), randint(0, Plane)])


def sex(genome1, genome2, Plane):
    a = genome1[-2:]
    b = genome2[-2:]
    if (a == b).all():
        og1 = genome1[2:5]
        og2 = genome2[2:5]
        oncogeneCount = np.count_nonzero(og1 == 20) + np.count_nonzero(og2 ==
                                                                       20)
        if oncogeneCount == 1:
            fertility = 1
            newRate1, newRate2 = inheritance(genome1[0], genome1[1],
                                             genome2[0], genome2[1])
            return daughter(genome1, genome2, newRate1, newRate2, Plane)
        elif oncogeneCount == 2:
            fertility = 3
            progArray = np.empty([3, 8], dtype=np.int)
            for n in range(fertility):
                newRate1, newRate2 = inheritance(genome1[0], genome1[1],
                                                 genome2[0], genome2[1])
                progeny = daughter(genome1, genome2, newRate1, newRate2, Plane)
                progArray[n] = progeny
            return progArray
        else:
            return []
    else:
        return []


def mate(genomes, Plane):
    daughterArray = np.zeros([1, 8], dtype=np.int)
    for i in range(len(genomes)):
        for j in range(i+1, len(genomes)):
            progeny = sex(genomes[i], genomes[j], Plane)
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


def predatorEndangered(predators, predSize, Plane, genomes):
    _Predators = predators
    while len(_Predators) < predSize:
        newp = np.random.randint(Plane+1, size=(1, 2))
        _Predators = np.vstack([_Predators, newp])
        if len(_Predators) >= len(genomes):
            break
    return _Predators


def predatorLevels(genomes, predators, predCurve, Plane):
    predSize = exponential(predCurve, len(genomes))
    if len(predators) > predSize:
        return predators[0:predSize]
    elif len(predators) < predSize:
        muchosPred = predatorEndangered(predators, predSize, Plane, genomes)
        return muchosPred
    else:
        return predators


def popMax(genomes, popMax):
    if len(genomes) > popMax:
        select = np.random.randint(len(genomes), size=popMax)
        return genomes[select, :]
    else:
        return genomes


def diversity(genomes, Plane, predCurve, High):
    replaceNum = int(0.1*len(genomes))
    for n in np.random.randint(0, high=len(genomes), size=replaceNum):
        genomes[n], discard = population(1, Plane, predCurve, High)


# predator population controlled by exp function y = a(b^x)+c where
# a = 1
# b = 1.025
# c = 1

def runSimulation(iters, OMR, predCurve, predRate, popStart, High, run, gen):
    genomes, predators = population(popStart, int(0.2*popStart), predCurve,
                                    High)
    predationRate = predRate
    popCap = 1000
    rateAvg = []
    populSize = []
    rateStd = []
    for n in range(iters):
        t0 = time.time()
        Plane = int(0.2*len(genomes))
        mutate(genomes, High)
        move(genomes, OMR, Plane)
        move(predators, OMR, Plane)
        predators = predatorLevels(genomes, predators, predCurve, Plane)
        child = mate(genomes, Plane)
        genomes = procreate(genomes, child)
        genomes = np.array(filter(cancer, genomes))

        def kill(genome):
            location = genome[-2:]
            if location.tolist() in predators.tolist():
                oncogenes = genome[2:5]
                oncogeneCount = np.count_nonzero(oncogenes == 20)
                if oncogeneCount == 2:
                    Prob = predationRate
                else:
                    Prob = predationRate*3
                return Prob <= uniform(0, 1)
            else:
                return True

        genomes = np.array(filter(kill, genomes))

        genomes = popMax(genomes, popCap)
        if n % 100 == 0:
            if len(genomes) > 0:
                diversity(genomes, Plane, predCurve, High)
        geno = False
        if len(genomes) <= 1:
            geno = True
            print("genocide")
            break
        ratesAll = meanRates(genomes[:, 0:2])
        rateAvg.append(np.mean(ratesAll))
        rateStd.append(np.std(ratesAll))
        populSize.append(len(genomes))
        if np.std(ratesAll) == 0:
            print("no diversity")
            break
        if np.max(genomes[:, 5]) >= gen:
            print("gen max reached")
            break
        t1 = time.time()
        if n % 10 == 0:
            print(run, n, t1-t0, int(np.mean(ratesAll)), int(np.std(ratesAll)),
                  len(genomes), len(predators), np.max(genomes[:, 5]), Plane)
    return ratesAll, rateAvg, rateStd, populSize, geno
