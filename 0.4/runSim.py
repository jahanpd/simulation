import matrixSim as ms
import os

# runSimulation(iters, organismMoveRate, predCurve, predRate, popStart, high)
# return ratesAll, rateAvg, rateStd, populSize

cycles = 1001
iters = 1001
maxRate = 100
doco = 0

while doco < cycles:
    ratesAll1, rateAvg1, rateStd1, popSize1, geno = \
        ms.runSimulation(iters, 1, 1.04, 0.4, 100, maxRate, doco)
    if geno is False:
        directory = "data"

        if not os.path.exists(directory):
            os.makedirs(directory)

        statsname = "data/statsRateAvg%s.txt" % doco
        statsExport = open(statsname, 'w')
        for n in rateAvg1:
            statsExport.write("%s," % n)
        statsExport.close()

        statsname = "data/statsEnd%s.txt" % doco
        statsExport = open(statsname, 'w')
        for n in rateAvg1:
            statsExport.write("%s," % n)
        statsExport.close()

        doco += 1
