from itertools import filterfalse
from math import isnan, sqrt
import os
from statistics import mean, variance
from PySide6.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np
import operator as op
from scipy import stats

def FindNearestNumber(arr, target):
        arr = np.array(arr)
        idx = (np.abs(arr - target)).argmin()
        return arr[idx]

class MplGraph(QWidget):
    def __init__(self, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.fig = Figure([5, 4], dpi=100)
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.canvas.axes = self.fig.add_subplot(111)
        self.toolbar = NavigationToolbar(self.canvas, parent)
        Vlayout = QVBoxLayout()
        Vlayout.addWidget(self.toolbar)
        Vlayout.addWidget(self.canvas)
        self.setLayout(Vlayout)

    def PlotLineGraph(self, plotDataMultilayers, value=0.5, axis = 'X'):
        slicedColumn = 0 if axis == 'X' else 1
        plotDatas = []
        means = []
        sdevs = []
        for i in range(len(plotDataMultilayers)):
            slicedColumnData = plotDataMultilayers[i][:, slicedColumn]
            nearestNumber = FindNearestNumber(slicedColumnData, value)
            rowsToBeDel = np.where(slicedColumnData != nearestNumber)[0]
            plotData = np.delete(plotDataMultilayers[i], rowsToBeDel, axis=0)
            plotDatas.append(plotData)
            nanRemoved = list(filterfalse(isnan, plotData[:, 2]))
            means.append(mean(nanRemoved))
            sdevs.append(sqrt(variance(nanRemoved)))
        
        plotDataStacked = np.vstack(tuple(plotDatas))
        plotter = self.canvas.axes 
        plotter.clear()
        plotter.scatter(plotDataStacked[:, 1] if axis == 'X' else plotDataStacked[:, 0],
                        plotDataStacked[:, 2], color='b',
                        label='Data Points',
                        marker='.', s=4)
        #plotter.plot(plot2dData[:,0], plot2dData[:, 2], color='b', label='Data Points', marker='.', markersize=4)
        self.canvas.draw()

    def plotNormalDistribution(self, data):
        plotter = self.canvas.axes 
        plotter.clear()
        mean = data.mean()
        sdev = data.std()
        for i in range(-3, 4):
            if i == 0: 
                plotter.axvline(mean, color='crimson', ls='--', lw=2, label='mean')
            else:
                plotter.axvline(mean+i*sdev, color='limegreen', ls='--', lw=2, label='mean + i*sdev' if i == 1 else None)
        
        data.sort()
        #snd = stats.norm(mean, sdev)
        #plotter.plot(data_cleaned, snd.pdf(data_cleaned), color='orange', lw=3, label='gaussian normal')
        binwidth = 5
        plotter.hist(data, bins=range(min(data) - 20, max(data) + 40, binwidth))
        plotter.autoscale(enable=True, axis='x', tight=True)
        plotter.legend()
        
        title = f'Histogram (Mean = {int(mean)}, STD = {sdev.__round__(3)})'
        plotter.set_title(title, fontsize='12')
        plotter.set_xlabel('Thickness values(um)', fontsize='13')
        plotter.set_ylabel('Frequency', fontsize='13')
        self.canvas.draw()

    def Plot3DPointCloud(self, plotData):
        x = plotData[:, 0]  
        y = plotData[:, 1]
        z = plotData[:, 2] 
        # Plot the surface.
        self._ax = self.canvas.figure.add_subplot(projection="3d")
        self._ax.plot_trisurf(x, y, z, cmap="viridis",
                        linewidth=0, antialiased=False)
        self.canvas.draw()

    def PlotGraphToImage(self, imageName):
        self.canvas.draw()
        ROOT_DIR =  os.path.abspath(os.path.join(".", os.curdir))
        fname = os.path.join(ROOT_DIR, "PlotImages\\" + imageName + ".png")
        from PIL import Image
        img = Image.new("RGB", (800, 1280), (255, 255, 255))
        img.save(fname, "PNG")
        self.canvas.print_png(fname)
        print("Mpl image created: ", fname)
        return fname
