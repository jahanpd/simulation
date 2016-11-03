import matplotlib.pyplot as plt
import matplotlib.animation as animation

def plot(Population):
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)

    def animate(i):
        pullX = open("X.txt", "r").read()
        pullY = open("Y.txt", "r").read()
        dataX = pullX.split('\n')
        dataY = pullY.split('\n')
        xar = []
        yar = []
        for Line in dataX:
            xar.append(int(Line))
        for Line in dataY:
            yar.append(int(Line))
        ax1.clear()
        ax1.scatter(xar, yar)
    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()
