import matplotlib.pyplot as plt
import matplotlib.animation as animation

def plot(Population):
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)

    def animate(i):
        xar = []
        yar = []
        for Organism in Population:
            X = int(Organism[-19:-10])
            Y = int(Organism[-9:])
            xar.append(int(X))
            yar.append(int(Y))
        ax1.clear()
        ax1.scatter(xar, yar)
    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()
