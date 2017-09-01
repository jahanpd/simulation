import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import matrixSim as ms

# runSimulation(iters, organismMoveRate, predCurve, predRate, popStart, high)
# return ratesAll, rateAvg, rateStd, populSize

cycles = 4
iters = 6000
maxRate = 1000

for run in range(cycles):
    ratesAll1, rateAvg1, rateStd1, popSize1, spread1 = \
        ms.runSimulation(iters, 1, 1.03, 1, 100, maxRate, run)

    ratesAll2, rateAvg2, rateStd2, popSize2, spread2 = \
        ms.runSimulation(iters, 1, 1.03, 0.5, 100, maxRate, run)

    highPred = plt.plot(range(len(rateAvg1)), rateAvg1, 'g-', label='high')
    lowPred = plt.plot(range(len(rateAvg2)), rateAvg2, 'r-', label='low')
    popHigh = plt.plot(range(len(popSize1)), popSize1, 'g-')
    popLow = plt.plot(range(len(popSize2)), popSize2, 'r-')

    rateAvg1 = np.array(rateAvg1)
    rateStd1 = np.array(rateStd1)
    rateAvg2 = np.array(rateAvg2)
    rateStd2 = np.array(rateStd2)
    plt.fill_between(range(len(rateAvg1)), rateAvg1+rateStd1,
                     rateAvg1-rateStd1)
    plt.fill_between(range(len(rateAvg2)), rateAvg2+rateStd2,
                     rateAvg2-rateStd2)
    fig1 = plt.gcf()
    plt.axis([0, iters, 0, maxRate])
    filename = "plot%s.png" % run
    fig1.savefig(filename)
    plt.close()

    n1, bins1, patches1 = plt.hist(ratesAll1, color='green', alpha=0.4)
    n2, bins2, patches2 = plt.hist(ratesAll2, color='red', alpha=0.4)
    y1 = mlab.normpdf(bins1, np.mean(ratesAll1), np.std(ratesAll1))
    y2 = mlab.normpdf(bins2, np.mean(ratesAll2), np.std(ratesAll2))
    histog1 = plt.plot(bins1, y1, 'g--', linewidth=1)
    histog2 = plt.plot(bins2, y2, 'r--', linewidth=1)
    histo1 = plt.gcf()
    plt.axis([0, 600, 0, 80])
    filename = "histo%s.png" % run
    histo1.savefig(filename)
    plt.close()
