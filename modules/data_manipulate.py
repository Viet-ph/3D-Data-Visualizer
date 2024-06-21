from widgets import *
from modules.gui_modules import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from Windows.layerSelctionWindow import LayerSelectionWindow
import numpy as np

def PlotLineGraphMatplotlib(plotWidget: MplGraph):
    plotData = PreprocessData()
    plotWidget.PlotLineGraph(plotData, 10)

# def PlotPointCloudPyVista(plotWidget: PyVistaWidget):
#     plotData = PreprocessData()
#     plotWidget.PlotPointCloud(plotData)

#Testing function
def PlotPointCloudMatplotlib(plotWidget: MplGraph):
    plotData = PreprocessData()
    plotWidget.Plot3DPointCloud(plotData)

#Testing function
def PlotScatterGraphQt(graphTable: QTableWidget):
    plotData = PreprocessData()
    scatter = ScatterGraph()
    minimum_graph_size = QSize(1000 / 2, 800 / 1.75)
    scatter.initialize(minimum_graph_size, QSize(1000,800))
    scatter.AddData(plotData)  
    #AppFunctions.AddGraphToTable(graphTable, graphImageView.label)

def PlotSurfaceGraphQt(mainWindow, dataTuple):
    AppFunctions.RenderSurfaceGraph(dataTuple, mainWindow)

def PlotHeatMapQt(mainWindow, dataTuple:tuple):
    print("plotting heatmap")
    fileNames, additionalParams = dataTuple
    for fileName in fileNames:
        AppFunctions.PlotHeatmapPlotly(fileName, additionalParams, mainWindow)


    
    





    

