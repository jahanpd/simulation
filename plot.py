import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)


def animate(i):
    pullX = open("X.txt", "r").read()
    pullY = open("Y.txt", "r").read()
    pullX = pullX.split('\n')
    pullY = pullY.split('\n')
    xar = []
    yar = []
    for Line in pullX:
        if len(Line) < 4:
            xar.append(int(Line))
    for Line in pullY:
        if len(Line) > 1:
            yar.append(int(Line))
    ax1.clear()
    ax1.scatter(xar, yar)
ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
