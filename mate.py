from random import randint
import itertools
from backBone import generatePopulations

Population, Predators = generatePopulations()

def sex(genomeOne, genomeTwo):
    locationOne = genomeOne[-10:]
    locationTwo = genomeTwo[-10:]
    if locationOne == locationTwo:
        rateOne = int(genomeOne[13:30],2)
        rateTwo = int(genomeTwo[13:30],2)
        newRate = int(rateOne + rateTwo)/2
        newGene = bin(newRate)
        newGenome = spawnGenome(newGene)
        Daughter.append(newGenome)

def mate(Population):
    Daughters = []
    for a, b in itertools.combinations(Population, 2):
        sex(a, b)
    return Daughters

sjsjs = mate(Population)
print(sjsjs)
