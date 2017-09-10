import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import matrixSim as ms
import os

# runSimulation(iters, organismMoveRate, predCurve, predRate, popStart, high)
# return ratesAll, rateAvg, rateStd, populSize

generations = 50
cycles = 100
iters = 1000
maxRate = 100
doco = 0

for gen in range(generations):
    for run in range(cycles):
        ratesAll1, rateAvg1, rateStd1, popSize1, geno = \
            ms.runSimulation(iters, 1, 1.030, 0.2, 100, maxRate, run, gen)
        if geno is False:
            directory = "gen%s" % gen
            if not os.path.exists(directory):
                os.makedirs(directory)
            statsname = "gen%s/statsEnd%s.txt" % (gen, doco)
            statsExport = open(statsname, 'w')
            for n in ratesAll1:
                statsExport.write("%s," % n)
            statsExport.close()

            doco += 1
