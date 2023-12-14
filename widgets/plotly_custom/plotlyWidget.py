from itertools import filterfalse
from math import isnan
import plotly.graph_objs as go
import numpy as np
from PySide6 import QtWidgets, QtWebEngineWidgets
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import QSize, QUrl, SignalInstance
from PySide6.QtDataVisualization import *
from widgets.mplwidget import MplGraph

def create_url(name):
    url = QUrl()
    url.setScheme(b"plotly".decode())
    url.setHost(name)
    return url

class PlotlyGraph(QWidget):
    graphNameAlias = {}
    def __init__(self, graphName, additionalParams, parent=None):
        super().__init__(parent)

        self._view = QtWebEngineWidgets.QWebEngineView()
        self.graphImage: QLabel = QLabel()
        self.graphName = graphName
        self._heatmapParams = additionalParams
        self._url = None
        self.fig: go.Figure = None

        self._mplGraph = MplGraph(self)
        self._mplGraph.setMinimumWidth(300)
        self._mplGraph.setMinimumHeight(300)
        self._mplGraph.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self._view)
        splitter.addWidget(self._mplGraph)
        hlay = QtWidgets.QHBoxLayout(self)
        hlay.addWidget(splitter)
        self.resize(1200, 800)
        self.setWindowTitle("HeatMap")

        PlotlyGraph.graphNameAlias[graphName] = 'heatmap' + str(len(PlotlyGraph.graphNameAlias))

    def ViewDetail(self):
        self.show()
        
    def RenderToImage(self, plotData, progress_callback: SignalInstance):
        progress_callback.emit(0, "Setting figure...")
        if self._heatmapParams is None:
            self.fig = go.Figure(data=go.Heatmap(x=plotData[:, 0] if len(plotData[:, 0]) > len(plotData[:, 1]) else plotData[:, 1],
                                                y=plotData[:, 1] if len(plotData[:, 1]) < len(plotData[:, 0]) else plotData[:, 0], 
                                                z=plotData[:, 2], 
                                                colorscale='jet'))
        else: 
            self.fig = go.Figure(data=go.Heatmap(x=plotData[:, 0] if len(plotData[:, 0]) > len(plotData[:, 1]) else plotData[:, 1],
                                                y=plotData[:, 1] if len(plotData[:, 1]) < len(plotData[:, 0]) else plotData[:, 0], 
                                                z=plotData[:, 2], zmin=self._heatmapParams["lowerLimit"], zmax= self._heatmapParams["upperLimit"],
                                                colorscale='jet'))
        
        # Set the axis and layout properties
        progress_callback.emit(10, "Setting axis...")
        self.fig.update_layout(title=self.graphName)#, xaxis_title="X", yaxis_title="Y")
        self.fig.update_traces(marker=dict(size=50,line=dict(width=2,color='DarkSlateGrey')),
                               selector=dict(mode='markers'))

        fileName = "PlotImages\\" + self.graphName + ".png"

        progress_callback.emit(25, "Plotting heatmap...")
        self.fig.write_image(fileName, 'png')
        print("Heatmap plotted")
        image = (QPixmap(fileName, flags=Qt.ImageConversionFlag.AutoColor)
                .scaled(QSize(400,300), Qt.AspectRatioMode.IgnoreAspectRatio,
                        Qt.TransformationMode.SmoothTransformation))
        print("Heatmap Image created")
        self.graphImage.setPixmap(image)
        print("Heatmap image set")
        self._url = create_url(PlotlyGraph.graphNameAlias[self.graphName])
        print("Url created")
        
        data_filtered = list(filterfalse(isnan, plotData[:, 2]))
        self._mplGraph.plotNormalDistribution(np.array([int(data * 1000) for data in data_filtered]))
        # self._view.load(url)
        # print("Url loaded")
        progress_callback.emit(100, "Done")

    def LoadUrl(self):
        self._view.load(self._url)

    def GetGraphImage(self) -> QLabel:
        return self.graphImage
