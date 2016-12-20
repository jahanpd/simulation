# n: [X,Y,Sex,birthday,alive,lifespan, generation, parity, starve, CoD ]
#     0,1,2  ,3       ,4    ,5       , 6         ,7      , 8       , 9
# 0=f and alive

# imported modules
from random import randint
from random import uniform
import time
import csv
import statistics
import matplotlib.pyplot as plt

# parameters
sps = 20    # starting population size
stt = time.time()  # defines start time
pr = 0.1    # proportion of predators to the living population
gen = 50    # the generation when to end
ls = 15     # lifespan in seconds
pp = 0.2    # likelihood of dying if person meets predator
xax = 0.5     # x axis modifyer
yax = 0.5     # y axis modifyer
fam = 100     # food amount modifier
sth = 4     # the amount each person is sated at beginning

pop_alive = {
    1: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

}

pop_dau = {}

pop_dead = {}

pop_pre = {}

food = []

eaten = []

agen = [0, ]

# Generate starting population
while len(pop_alive) != sps:
    pop_alive[len(pop_alive) + 1] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Generate coordinate location for X and Y, as well as sex, birthday, and ls
for X in pop_alive:
    pop_alive[X][0] = randint(0, int(xax*len(pop_alive)))
    pop_alive[X][1] = randint(0, int(yax*len(pop_alive)))
    pop_alive[X][2] = randint(0, 1)
    pop_alive[X][3] = time.time()
    pop_alive[X][5] = ls
    pop_alive[X][6] = 0
    pop_alive[X][7] = 0
    pop_alive[X][8] = sth

cgen = 0
# START LOOP
while True:
    # Generate food on map
    while len(food) < fam*len(pop_alive):
        xaf = randint(0, int(xax*len(pop_alive)))
        yaf = randint(0, int(yax*len(pop_alive)))
        food.append([xaf, yaf])

    # ensure food is in map
    for loc in range(0, len(food)):
        xpf = food[loc][0]
        ypf = food[loc][1]
        if xpf > int(xax*len(pop_alive)):
            food[loc][0] = randint(0, int(xax*len(pop_alive)))
        if ypf > int(xax*len(pop_alive)):
            food[loc][1] = randint(0, int(yax*len(pop_alive)))

    # Generate the predator population
    while len(pop_pre) < int(pr*len(pop_alive)):
        key = 1 + len(pop_pre)
        pop_pre[key] = [0, 0, 0]
        pop_pre[key][0] = randint(0, int(xax*len(pop_alive)))
        pop_pre[key][1] = randint(0, int(yax*len(pop_alive)))

    # ensure the predator population is the right size
    for pre in pop_pre:
        if len(pop_pre) > int(pr*len(pop_alive)):
            eaten.append(pre)
    pop_pre = {i: pop_pre[i] for i in pop_pre if i not in eaten}
    eaten = []

    # see who is available to mate and mate them.
    for man in pop_alive:
        if pop_alive[man][2] == 1:
            xm = pop_alive[man][0]
            ym = pop_alive[man][1]
            for fem in pop_alive:
                if pop_alive[fem][2] == 0:
                    xf = pop_alive[fem][0]
                    yf = pop_alive[fem][1]
                    if xm == xf and ym == yf:
                        key = 1 + len(pop_alive) + len(pop_dead) + len(pop_dau)
                        pop_dau[key] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                        pop_dau[key][0] = randint(0, int(xax*len(pop_alive)))
                        pop_dau[key][1] = randint(0, int(yax*len(pop_alive)))
                        pop_dau[key][2] = randint(0, 1)
                        pop_dau[key][3] = time.time()
                        avls = (pop_alive[fem][5] + pop_alive[man][5])/2
                        pop_dau[key][5] = uniform(avls - 1, avls + 1)
                        nextgen = pop_alive[fem][6]
                        pop_dau[key][6] = nextgen + 1
                        pop_alive[fem][7] += 1

    # for breaking at the right generation
    if len(pop_dau) > 1:
        key = len(pop_alive) + len(pop_dead) + len(pop_dau)
        if pop_dau[key][6] not in agen:
            agen.append(pop_dau[key][6])

    # consolidate populations after mating
    for dau in pop_dau:
        pop_alive[dau] = pop_dau[dau]

    pop_dau = {i: pop_dau[i] for i in pop_dau if i not in pop_alive}

    # eating like a king
    for nom in pop_alive:
        xn = pop_alive[nom][0]
        yn = pop_alive[nom][1]
        coord = [xn, yn]
        if coord in food:
            eaten.append(coord)
            pop_alive[nom][8] += 1
        else:
            pop_alive[nom][8] -= 1
            if pop_alive[nom][8] < 0:
                pop_alive[nom][4] == 1
                pop_alive[nom][9] = 'S'
                pop_dead[nom] = pop_alive[nom]
    pop_alive = {i: pop_alive[i] for i in pop_alive if i not in pop_dead}
    food = [i for i in food if i not in eaten]
    eaten = []

    # killing with predators
    for pre in pop_pre:
        xp = pop_pre[pre][0]
        yp = pop_pre[pre][1]
        for vic in pop_alive:
            xv = pop_alive[vic][0]
            yv = pop_alive[vic][1]
            if xp == xv and yp == yv:
                if uniform(0, 1) < pp:
                    pop_alive[vic][4] = 1
                    pop_alive[vic][9] = 'P'
                    pop_dead[vic] = pop_alive[vic]
    pop_alive = {i: pop_alive[i] for i in pop_alive if i not in pop_dead}

    # killing with lifespan
    for liv in pop_alive:
        age = time.time() - pop_alive[liv][3]
        lsp = pop_alive[liv][5]
        if age > lsp:
            pop_alive[liv][4] = 1
            pop_alive[liv][9] = 'L'
            pop_dead[liv] = pop_alive[liv]

    # list comprehension to get corpses out of the living population
    pop_alive = {i: pop_alive[i] for i in pop_alive if i not in pop_dead}

    # move them rude boiz around
    for liv in pop_alive:
        xl = pop_alive[liv][0]
        yl = pop_alive[liv][1]
        pop_alive[liv][0] = randint(xl - 1, xl + 1)
        pop_alive[liv][1] = randint(yl - 1, yl + 1)
        if pop_alive[liv][0] > int(xax*len(pop_alive)):
            pop_alive[liv][0] = int(xax*len(pop_alive)) - 1
        elif pop_alive[liv][0] < 0:
            pop_alive[liv][0] = 1
        if pop_alive[liv][1] > int(yax*len(pop_alive)):
            pop_alive[liv][1] = int(yax*len(pop_alive)) - 1
        elif pop_alive[liv][1] < 0:
            pop_alive[liv][1] = 1
    for pre in pop_pre:
        xpm = pop_pre[pre][0]
        ypm = pop_pre[pre][0]
        pop_pre[pre][0] = randint(xpm - 1, xpm + 1)
        pop_pre[pre][1] = randint(ypm - 1, ypm + 1)
        if pop_pre[pre][0] > int(xax*len(pop_alive)):
            pop_pre[pre][0] = int(xax*len(pop_alive)) - 1
        elif pop_pre[pre][0] < 0:
            pop_pre[pre][0] = 1
        if pop_pre[pre][1] > int(yax*len(pop_alive)):
            pop_pre[pre][1] = int(yax*len(pop_alive)) - 1
        elif pop_pre[pre][1] < 0:
            pop_pre[pre][1] = 1

    if len(pop_alive) == 0:
        print "everyone died!"
        break

    if len(pop_alive) == 200:
        print "pop 200"
        break
    if max(agen) > gen:
        print "finished!"
        break
 
    print 'pop: %s and gen: %s' % (len(pop_alive), max(agen))
"""
    # graphing positions
    plox_pa = []
    ploy_pa = []
    plox_pp = []
    ploy_pp = []
    for p in pop_alive:
        plox_pa.append(pop_alive[p][0])
        ploy_pa.append(pop_alive[p][1])
    for p in pop_pre:
        plox_pp.append(pop_alive[p][0])
        ploy_pp.append(pop_alive[p][1])

    plt.plot([plox_pa], [ploy_pa], 'g^', [plox_pp], [ploy_pp], 'ro')
    plt.axis([0, int(xax*len(pop_alive)), 0, int(yax*len(pop_alive))])
    plt.show()
    plt.pause(0.0001)"""

# END LOOP

# Create dictionary of lifespans from pop_alive
stats = []
for sur in pop_alive:
    stats.append(pop_alive[sur][5])

dstats = []
for sur in pop_dead:
    dstats.append(pop_dead[sur][5])

av_lsp = statistics.mean(stats)
print av_lsp
sd_lsp = statistics.stdev(stats)
print sd_lsp

av_lsp = statistics.mean(dstats)
print av_lsp
sd_lsp = statistics.stdev(dstats)
print sd_lsp

stats = []
for sur in pop_alive:
    stats.append({'lifespan': pop_alive[sur][5]})

# export to csv file
fieldnames = ['lifespan', 'Cause of Death']
rel_stat = open('stats,csv', 'wb')
csvwriter = csv.DictWriter(rel_stat, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn, fn) for fn in fieldnames))
for row in stats:
    csvwriter.writerow(row)
rel_stat.close()

print food
print eaten
print pop_alive
print pop_pre
print pop_dau
print len(pop_dead)
