# Copyright (C) 2023 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

from itertools import filterfalse
from math import cos, degrees, isnan, nan, sqrt
from statistics import mean
import numpy as np
import copy
from PySide6.QtCore import QObject, Signal, Slot, Qt, QSize
from PySide6.QtGui import *
from PySide6.QtWidgets import QAbstractSlider, QLabel
from PySide6.QtDataVisualization import (QAbstract3DGraph, QAbstract3DSeries,
                                         QScatterDataItem, QScatterDataProxy,
                                         QScatter3DSeries, Q3DCamera, Q3DScatter,
                                         Q3DTheme)

from .axesinputhandler import AxesInputHandler
from widgets.mplwidget import MplGraph

class ScatterDataModifier(QObject):
    def __init__(self, scatter: Q3DScatter, lineGraph: MplGraph, parent, dataFrames):
        super().__init__(parent)

        self._graph = scatter
        self._lineGraph = lineGraph
        #self._textField = label

        self.surfaceImage: QLabel = QLabel()
        self.matPlotlibImage: QLabel = QLabel()

        self._flatPLaneProxy = QScatterDataProxy()
        self._flatPlaneSeries = QScatter3DSeries(self._flatPLaneProxy)
        self._flatPlaneDataArray = None

        self._layersSeries = []
        self._dataArrays = []
        self._plotDatas = dataFrames
        self._totalLayers = len(dataFrames)

        self._slicingPlaneSelectedValue = 0

        self._axisMinSliderX = None
        self._axisMaxSliderX = None
        self._axisMinSliderZ = None
        self._axisMaxSliderZ = None
        self._flatPlaneSlider = None
        self._rangeMinX = 0.0
        self._rangeMinZ = 0.0
        self._rangeMinY = 0.0
        self._rangeMaxX = 0.0
        self._rangeMaxZ = 0.0
        self._rangeMaxY = 0.0
        self._sampleCount = 0
        self._stepX = 0.0
        self._stepZ = 0.0
        self._totalStepsX = 0
        self._totalStepsZ = 0

        self._selectionAnimation = None
        self._titleLabel = None
        self._previouslyAnimatedItem = None
        self._previousScaling = {}

        #self._graph.setAspectRatio = 4
        self._graph.setHorizontalAspectRatio = 0.0

        self._style = QAbstract3DSeries.Mesh.MeshSphere
        self._smooth = False
        self._inputHandler = AxesInputHandler(scatter, self._lineGraph)
        self._autoAdjust = True

        self._graph.activeTheme().setType(Q3DTheme.ThemeQt)
        self._graph.setShadowQuality(QAbstract3DGraph.ShadowQualityNone)
        self._graph.scene().activeCamera().setCameraPreset(Q3DCamera.CameraPresetDirectlyAboveCW45)
        self._graph.scene().activeCamera().setZoomLevel(120.0)
        
        self._sampleCount = 0

        # Give ownership of the handler to the graph and make it the active
        # handler
        self._graph.setActiveInputHandler(self._inputHandler)

        # Give our axes to the input handler
        self._inputHandler.setAxes(self._graph.axisX(), self._graph.axisZ(),
                                    self._graph.axisY())
        self._inputHandler.setRotationEnabled(False)

    def SetPlotData(self, plotData):
        self._plotData = plotData
        self.fillMultiLayerData()
        self.addSeries()

    def GetPlotData(self):
        return self._plotData

    def fillMultiLayerData(self):
        # Configure the axes according to the data
        dataFrames = []
        for i in range(self._totalLayers):
            self._layersSeries.append(QScatter3DSeries(QScatterDataProxy()))
            self._dataArrays.append([])
            x_list = self._plotDatas[i][:, 0]
            y_list = self._plotDatas[i][:, 2]
            z_list = self._plotDatas[i][:, 1]
            values, counts = np.unique(list(filterfalse(isnan, y_list)), return_counts=True)
            ind = np.argmax(counts)
            dataFrame = dict(x     = x_list,
                             y     = y_list,
                             z     = z_list,
                             x_min = min(x_list),
                             y_min = min(list(filterfalse(isnan, y_list))),
                             z_min = min(z_list),
                             x_max = max(x_list),
                             y_max = max(list(filterfalse(isnan, y_list))),
                             z_max = max(z_list),
                             y_avg = mean(list(filterfalse(isnan, y_list))),
                             y_mode = values[ind])
            print(dataFrame['y_avg'])
            dataFrames.append(dataFrame)
        
        self._rangeMinX = min([dataFrame['x_min'] for dataFrame in dataFrames])
        self._rangeMinZ = min([dataFrame['z_min'] for dataFrame in dataFrames])
        self._rangeMinY = min([dataFrame['y_min'] for dataFrame in dataFrames])
        self._rangeMaxX = max([dataFrame['x_max'] for dataFrame in dataFrames])
        self._rangeMaxZ = max([dataFrame['z_max'] for dataFrame in dataFrames])
        self._rangeMaxY = max([dataFrame['y_max'] for dataFrame in dataFrames])

        print("Min x: ", self._rangeMinX)
        print("Max x:", self._rangeMaxX)
        print("Min z: ", self._rangeMinZ)
        print("Max z:", self._rangeMaxZ)
        print("Min y: ", self._rangeMinY)
        print("Max y:", self._rangeMaxY)
        print("Avg y:", dataFrames[0]['y_avg'])
        print("Mode y:", dataFrames[0]['y_mode'])

        z = dataFrames[0]['z']
        x = dataFrames[0]['x']
        y_collection = [frame['y'] for frame in dataFrames]
    
        self._totalStepsX = len(dict.fromkeys(x))
        self._totalStepsZ = len(dict.fromkeys(z))
         # Reset range sliders
        self._stepX = float((self._rangeMaxX - self._rangeMinX) / float(self._totalStepsX - 1)).__round__(3)
        self._stepZ = float((self._rangeMaxZ - self._rangeMinZ) / float(self._totalStepsZ - 1)).__round__(3)
        print("Step x: ", self._stepX)
        print("Step z: ", self._stepZ)

        print("steps x: ", self._totalStepsX)
        print("steps z: ", self._totalStepsZ)
        print("steps y: ", len(dataFrames[0]['y']))

        for i in range(self._totalStepsZ):
            for j in range(self._totalStepsX):
                for layerIndex in range(self._totalLayers):
                    y = y_collection[layerIndex]
                    y_avg = dataFrames[layerIndex]['y_avg']
                    index = j + i * self._totalStepsX
                    x_val = self._rangeMinX + j * self._stepX
                    z_val = self._rangeMinZ + i * self._stepZ
                    dataPoint = QScatterDataItem(QVector3D(x_val,
                                                           y[index] if y[index] > y_avg else nan,
                                                           z_val))
                    for layerIndex in range(self._totalLayers):
                        self._dataArrays[layerIndex].append(dataPoint)
                    self._sampleCount += 1
            
        print(f"{i + 1} row added")
        self.fillDataForFlatPlane('Z')
        print("data added")

        self.SetProxiesArray()

    def fillDataForFlatPlane(self, axis, value = 0):
        self._flatPlaneDataArray = []
        if axis == "Z":
            #Create a grid-like surface by adding data points
            z_plane = self._rangeMinZ + (self._rangeMaxZ - self._rangeMinZ) / 2 if value == 0 else value
            self._slicingPlaneSelectedValue = z_plane
            step_y = (self._rangeMaxY - self._rangeMinY) / 4
            step_x = (self._rangeMaxX - self._rangeMinX) / 4
            for y_coord in np.arange(self._rangeMinY, self._rangeMaxY + step_y, step_y):
                for x_coord in np.arange(self._rangeMinX, self._rangeMaxX + step_x, step_x):
                    item = QScatterDataItem((QVector3D(x_coord, y_coord, z_plane)))
                    self._flatPlaneDataArray.append(item)
        else:
            #Create a grid-like surface by adding data points
            x_plane = self._rangeMinX + (self._rangeMaxX - self._rangeMinX) / 2 if value == 0 else value
            self._slicingPlaneSelectedValue = z_plane
            step_y = (self._rangeMaxY - self._rangeMinY) / 4
            step_z = (self._rangeMaxZ - self._rangeMinZ) / 4
            for y_coord in np.arange(self._rangeMinY, self._rangeMaxY + step_y, step_y):
                for z_coord in np.arange(self._rangeMinZ, self._rangeMaxZ + step_z, step_z):
                    item = QScatterDataItem((QVector3D(x_plane, y_coord, z_coord)))
                    self._flatPlaneDataArray.append(item)
    
    def addSeries(self):
        for layerSeries in self._layersSeries:
            layerSeries.setItemLabelFormat("@xTitle: @xLabel @yTitle: @yLabel @zTitle: @zLabel")
            layerSeries.setMeshSmooth(self._smooth)
            self._graph.addSeries(layerSeries)

        self._flatPlaneSeries.setMeshSmooth(self._smooth)
        self._graph.addSeries(self._flatPlaneSeries)
        self.setBlackToYellowGradient()
        
        print("Series added")
    
    def setFlatPlaneSlider(self, slider):
        self._flatPlaneSlider = slider

    # Function to update the line's position based on the slider value
    def update_line_position(self, value, axis):
        self.fillDataForFlatPlane(axis, value)
        self._flatPLaneProxy.resetArray(self._flatPlaneDataArray)

    def PlotLineGraph(self):
        self._lineGraph.PlotLineGraph(self._plotDatas, self._slicingPlaneSelectedValue)

    def RenderSurfaceToImage(self, imageName):
        image = self._graph.renderToImage(0, QSize(400, 300)).transformed(QTransform(), Qt.TransformationMode.SmoothTransformation)
        self.surfaceImage.setPixmap(QPixmap(image).transformed(QTransform(), Qt.TransformationMode.SmoothTransformation))
        (self._graph.renderToImage(0, QSize(1600, 1200))
                    .transformed(QTransform(), Qt.TransformationMode.SmoothTransformation)
                    .save("PlotImages\\" + imageName + "-3D" + ".png", None, 100))


    def RenderMatplotlibImage(self, imageName):
        image = QPixmap(self._lineGraph.PlotGraphToImage(imageName + "-2D sliced"), flags=Qt.ImageConversionFlag.AutoColor)
        image = image.scaled(QSize(400,300), Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.matPlotlibImage.setPixmap(image)
    
    def RenderGraphImages(self, graphName):
        self.RenderMatplotlibImage(graphName)
        self.RenderSurfaceToImage(graphName)

    def onFlatPlaneSliderChange(self, value, axis = 'Z'):
        if axis == 'Z':
            step = self._stepZ
            rangeMax = self._rangeMaxZ
            rangeMin = self._rangeMinZ
        else: 
            step = self._stepX
            rangeMax = self._rangeMaxX
            rangeMin = self._rangeMinX

        newValue = step * float(value)
        if newValue > rangeMax:
            newValue = rangeMax
        if newValue < rangeMin:
            newValue = rangeMin
        self.update_line_position(newValue, axis)
        self._slicingPlaneSelectedValue = newValue
        format_float = "{:.2f}".format(newValue)
        text = "Selected value: " + format_float
        #self._textField.setText(text)
    
    def SlideUpOne(self):
        self._flatPlaneSlider.triggerAction(QAbstractSlider.SliderAction.SliderPageStepAdd)

    def SlideDownOne(self):
        self._flatPlaneSlider.triggerAction(QAbstractSlider.SliderAction.SliderPageStepSub)

    def OrthogonalProjection(self, checked):
        self._graph.setOrthoProjection(checked)

    def SetProxiesArray(self):
        self._flatPLaneProxy.resetArray(self._flatPlaneDataArray)
        
        for i in range(self._totalLayers):
            self._layersSeries[i].dataProxy().resetArray(self._dataArrays[i])               

    def ResetDataArray(self):
        self._flatPLaneProxy.resetArray([])
        for i in range(self._totalLayers):
            self._layersSeries[i].dataProxy().resetArray([])  

    def setBlackToYellowGradient(self):
        gr = QLinearGradient()

        gr.setColorAt(0.0, Qt.black)
        gr.setColorAt(0.2, Qt.blue)
        gr.setColorAt(0.4, Qt.cyan)
        gr.setColorAt(0.6, Qt.green)
        gr.setColorAt(0.8, Qt.yellow)
        gr.setColorAt(1.0, Qt.red)

        self._flatPlaneSeries.setBaseGradient(gr)

        for layerSeries in self._layersSeries:
            layerSeries.setBaseGradient(gr)
            layerSeries.setColorStyle(Q3DTheme.ColorStyleRangeGradient)

        self._flatPlaneSeries.setColorStyle(Q3DTheme.ColorStyleRangeGradient)

    def setGreenToRedGradient(self):
        gr = QLinearGradient()
        gr.setColorAt(0.0, Qt.darkGreen)
        gr.setColorAt(0.5, Qt.yellow)
        gr.setColorAt(0.8, Qt.red)
        gr.setColorAt(1.0, Qt.darkRed)

        self._layer1Series.setBaseGradient(gr)
        self._layer1Series.setColorStyle(Q3DTheme.ColorStyleRangeGradient)

        for layerSeries in self._layersSeries:
            layerSeries.setBaseGradient(gr)
            layerSeries.setColorStyle(Q3DTheme.ColorStyleRangeGradient)  
    
    @Slot(int)
    def changeStyle(self, style):
        comboBox = self.sender()
        if comboBox:
            self._style = comboBox.itemData(style)
            if self._graph.seriesList():
                self._graph.seriesList()[0].setMesh(self._style)

    @Slot(int)
    def setSmoothDots(self, smooth):
        self._smooth = smooth == Qt.Checked.value
        series = self._graph.seriesList()[0]
        series.setMeshSmooth(self._smooth)

    @Slot(int)
    def changeTheme(self, theme):
        currentTheme = self._graph.activeTheme()
        currentTheme.setType(Q3DTheme.Theme(theme))
        self.backgroundEnabledChanged.emit(currentTheme.isBackgroundEnabled())
        self.gridEnabledChanged.emit(currentTheme.isGridEnabled())

    @Slot()
    def changePresetCamera(self):
        preset = Q3DCamera.CameraPresetFrontLow.value

        camera = self._graph.scene().activeCamera()
        camera.setCameraPreset(Q3DCamera.CameraPreset(preset))

        preset += 1
        if preset > Q3DCamera.CameraPresetDirectlyBelow.value:
            preset = Q3DCamera.CameraPresetFrontLow.value


    @Slot(int)
    def setGridEnabled(self, enabled):
        self._graph.activeTheme().setGridEnabled(enabled == Qt.Checked.value)

    def toggleModeNone(self):
        self._graph.setSelectionMode(QAbstract3DGraph.SelectionNone)
        print("None toggled")

    def toggleModeItem(self):
        self._graph.setSelectionMode(QAbstract3DGraph.SelectionItem)
        print("None toggled")


    def toggleModeSliceRow(self):
        sm = QAbstract3DGraph.SelectionRow
        self._graph.setSelectionMode(sm)
        print("None toggled")


    def toggleModeSliceColumn(self):
        sm = QAbstract3DGraph.SelectionColumn
        self._graph.setSelectionMode(sm)
