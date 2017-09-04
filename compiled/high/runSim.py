import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import matrixSim as ms

# runSimulation(iters, organismMoveRate, predCurve, predRate, popStart, high)
# return ratesAll, rateAvg, rateStd, populSize

cycles = 1000
iters = 1000
maxRate = 100
doco =  0

for run in range(cycles):
    ratesAll1, rateAvg1, rateStd1, popSize1, geno = \
        ms.runSimulation(iters, 1, 1.04, 0.95, 100, maxRate, run)
    if geno is False:
        statsname = "statsRateAvg%s.txt" % doco
        statsExport = open(statsname, 'w')
        for n in rateAvg1:
            statsExport.write("%s," % n)
        statsExport.close()
        doco += 1
