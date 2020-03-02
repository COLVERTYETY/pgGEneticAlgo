import matplotlib.pyplot as plt
import numpy as np

plt.ion() # make matplotlib interactif

class plotter():
    def __init__(self):
        self.fig = plt.figure()
        self.gs = self.fig.add_gridspec(3,1)
        self.ax1 = self.fig.add_subplot(self.gs[0, 0])
        self.ax2 = self.fig.add_subplot(self.gs[1,0])
        self.ax3 = self.fig.add_subplot(self.gs[2, 0])

    def update(self,EVOLUTIONMAX,EVOLUTIONAVG,best_weights,BEST_W8):
        self.ax3.clear()
        self.ax2.clear()
        self.ax1.clear()
        self.ax3.plot(EVOLUTIONMAX,label='max')
        self.ax3.plot(EVOLUTIONAVG,label='average')
        self.ax3.legend()
        best_weights = np.around(best_weights,decimals = 3)
        ttmp = best_weights.T
        self.ax2.imshow(ttmp)
        self.ax2.set_title("best brain of current gen")
        for i in range(len(ttmp)):
            for j in range(len(ttmp[0])):
                self.ax2.text(j, i, ttmp[i, j],
                    ha="center", va="center", color="w")
        tmpwaights = np.around(best_weights-BEST_W8,decimals = 3).T
        self.ax1.imshow(tmpwaights)
        self.ax1.set_title("change of best brain")
        for i in range(len(tmpwaights)):
            for j in range(len(tmpwaights[0])):
                self.ax1.text(j, i, tmpwaights[i, j],
                    ha="center", va="center", color="w")
        plt.draw()
        plt.pause(0.01)
        return best_weights