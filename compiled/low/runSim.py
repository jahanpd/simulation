import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import matrixSim as ms

# runSimulation(iters, organismMoveRate, predCurve, predRate, popStart, high)
# return ratesAll, rateAvg, rateStd, populSize

cycles = 1000
iters = 1000
maxRate = 100
means = []
doco = 0

for run in range(cycles):
    ratesAll1, rateAvg1, rateStd1, popSize1, geno = \
        ms.runSimulation(iters, 1, 1.030, 0.2, 100, maxRate, run)

    if geno is False:
        means.append(np.mean(ratesAll1))
        statsname = "statsEnd%s.txt" % doco
        statsExport = open(statsname, 'w')
        for n in ratesAll1:
            statsExport.write("%s," % n)
        statsExport.close()

        statsname = "statsRateAvg%s.txt" % doco
        statsExport = open(statsname, 'w')
        for n in ratesAll1:
            statsExport.write("%s," % n)
        statsExport.close()

        doco += 1

means = np.array(means)
n1, bins1, patches1 = plt.hist(means, color='green', alpha=0.4)
histog1 = plt.plot(bins1)
histo1 = plt.gcf()
plt.axis([0, maxRate, 0, 0.7*len(means)])
filename = "histoMeans.png"
histo1.savefig(filename)
plt.close()
