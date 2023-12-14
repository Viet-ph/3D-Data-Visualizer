# Copyright (C) 2023 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

from math import isnan, sqrt

import numpy as np
from configurations import config_global
from memory_profiler import profile
from math import nan
from modules.pyside_packages import *
from widgets.mplwidget import MplGraph

class SurfaceGraphModifier(QObject):
    def __init__(self, surface: Q3DSurface, label, lineGraph: MplGraph, parent, dataFrames, layerParams):
        super().__init__(parent)
        self._graph = surface
        self._lineGraph = lineGraph
        self._textField = label

        self.surfaceImage: QLabel = QLabel()
        self.matPlotlibImage: QLabel = QLabel()

        self._flatPLaneProxy = QSurfaceDataProxy()
        self._flatPlaneSeries = QSurface3DSeries(self._flatPLaneProxy)
        self._flatPlaneDataArray = None

        self._layersSeries = []
        self._dataArrays = []
        self._statistics = []
        self._plotDatas = dataFrames
        self._totalLayers = len(dataFrames)
        self._layerParams = layerParams

        self._slicingPlaneSelectedValue = 0
        self._selectedAxisForSlicing = 'X'

        self._axisMinSliderX = None
        self._axisMaxSliderX = None
        self._axisMinSliderZ = None
        self._axisMaxSliderZ = None
        self._axisMinSliderY = None
        self._axisMaxSliderY = None
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
        self._stepY = 0.001
        self._totalStepsX = 0
        self._totalStepsZ = 0
        self._totalStepsY = 0

        self._selectionAnimation = None
        self._titleLabel = None
        self._previouslyAnimatedItem = None
        self._previousScaling = {}

        self._customInputHandler = None
        self._defaultInputHandler = Q3DInputHandler()

        ac = self._graph.scene().activeCamera()
        ac.setZoomLevel(90)
        ac.setCameraPreset(Q3DCamera.CameraPresetIsometricRight)
        self._graph.activeTheme().setType(Q3DTheme.ThemeQt)

        self._x_axis = QValue3DAxis()
        self._y_axis = QValue3DAxis()
        self._z_axis = QValue3DAxis()
        self._graph.setAxisX(self._x_axis)
        self._graph.setAxisY(self._y_axis)
        self._graph.setAxisZ(self._z_axis)

        # Custom items and label
        self._graph.selectedElementChanged.connect(self.handleElementSelected)

        self._selectionAnimation = QPropertyAnimation(self)
        self._selectionAnimation.setPropertyName(b"scaling")
        self._selectionAnimation.setDuration(500)
        self._selectionAnimation.setLoopCount(-1)

        titleFont = QFont("Century Gothic", 30)
        titleFont.setBold(True)

    def fillMultiLayerData(self):
        config = config_global.config
        dataFrames = []
        for i in range(self._totalLayers):
            self._layersSeries.append(QSurface3DSeries(QSurfaceDataProxy()))
            self._dataArrays.append([])
            rawData, statistics = self._plotDatas[i]
            x_list = rawData[:, 0]
            y_list = rawData[:, 2]
            z_list = rawData[:, 1]
            dataFrame = dict(x     = x_list,
                             y     = y_list,
                             z     = z_list)
            dataFrames.append(dataFrame)
            self._statistics.append(statistics)
        
        self._rangeMinX = min([layerStatistics['x_min'] for layerStatistics in self._statistics])
        self._rangeMinZ = min([layerStatistics['z_min'] for layerStatistics in self._statistics])
        self._rangeMaxX = max([layerStatistics['x_max'] for layerStatistics in self._statistics])
        self._rangeMaxZ = max([layerStatistics['z_max'] for layerStatistics in self._statistics])

        if self._totalLayers > 1:
            self._rangeMinY = min([layerStatistics['y_min'] for layerStatistics in self._statistics])
            self._rangeMaxY = max([layerStatistics['y_max'] for layerStatistics in self._statistics])
        else:
            self._rangeMinY = self._layerParams["lowerLimit"]
            self._rangeMaxY = self._layerParams["upperLimit"]

        print("Min x: ", self._rangeMinX)
        print("Max x:", self._rangeMaxX)
        print("Min z: ", self._rangeMinZ)
        print("Max z:", self._rangeMaxZ)
        print("Min y: ", self._rangeMinY)
        print("Max y:", self._rangeMaxY)
        print("Avg y:", self._statistics[0]['y_avg'])

        z = [frame['z'] for frame in dataFrames]
        x = [frame['x'] for frame in dataFrames]
        y_collection = [frame['y'] for frame in dataFrames]
    
        self._totalStepsX = len(dict.fromkeys(x[0]))
        self._totalStepsZ = len(dict.fromkeys(z[0]))
        self._totalStepsY = int((self._rangeMaxY - self._rangeMinY) / self._stepY) + 1
        print("Total steps x: ", self._totalStepsX)
        print("Total steps z: ", self._totalStepsZ)

         # Reset range sliders
        self._stepX = float((self._rangeMaxX - self._rangeMinX) / float(self._totalStepsX - 1))
        self._stepZ = float((self._rangeMaxZ - self._rangeMinZ) / float(self._totalStepsZ - 1))
        print("Step x: ", self._stepX)
        print("Step z: ", self._stepZ)

        print("steps x: ", self._totalStepsX)
        print("steps z: ", self._totalStepsZ)
        print("steps y: ", len(dataFrames[0]['y']))

        for i in range(self._totalStepsZ):
            newRows = [[] for _ in range(self._totalLayers)]
            for j in range(self._totalStepsX):
                for layerIndex in range(self._totalLayers): 
                    y = y_collection[layerIndex]
                    y_avg = self._statistics[layerIndex]['y_avg']
                    index = j + i * self._totalStepsX
                    if index > len(y) - 1:  index = len(y) - 1
                    x_val = x[layerIndex][index]
                    z_val = z[layerIndex][index]
                    y_val = y[index] if y[index] > self._rangeMinY and y[index] < self._rangeMaxY else nan
                    # y_val = y[index] if abs(y[index] - y_avg) < config['Variance'] else(
                    #     y[index - 1] if config['FillHole'] else nan)
                    dataPoint = QSurfaceDataItem(QVector3D(x_val, y_val, z_val))
                    newRows[layerIndex].append(dataPoint)
                    self._sampleCount += 1
            for layerIndex in range(self._totalLayers):
                self._dataArrays[layerIndex].append(newRows[layerIndex])
        print(f"{i + 1} row added")
        self.fillDataForFlatPlane()
        print("data added")

        self.SetProxiesArray()

    def fillDataForFlatPlane(self, value = 0):
        self._flatPlaneDataArray = []
        currentMaxY = self._graph.axisY().max()
        currentMinY = self._graph.axisY().min()
        step_y = (currentMaxY - currentMinY) / 4
        if self._selectedAxisForSlicing == "Z":
            #Create a grid-like surface by adding data points
            z_plane = self._rangeMinZ + (self._rangeMaxZ - self._rangeMinZ) / 2 if value == 0 else value
            self._slicingPlaneSelectedValue = z_plane
            step_x = (self._rangeMaxX - self._rangeMinX) / 4
            for y_coord in np.arange(currentMinY, currentMaxY + step_y, step_y):
                newRow1 = []
                for x_coord in np.arange(self._rangeMinX, self._rangeMaxX + step_x, step_x):
                    item = QSurfaceDataItem((QVector3D(x_coord, y_coord, z_plane)))
                    newRow1.append(item)
                self._flatPlaneDataArray.append(newRow1)
        else:
            #Create a grid-like surface by adding data points
            x_plane = self._rangeMinX + (self._rangeMaxX - self._rangeMinX) / 2 if value == 0 else value
            self._slicingPlaneSelectedValue = x_plane
            step_z = (self._rangeMaxZ - self._rangeMinZ) / 4
            for z_coord in np.arange(self._rangeMinZ, self._rangeMaxZ + step_z, step_z):
                newRow1 = []
                for y_coord in np.arange(currentMinY, currentMaxY + step_y, step_y):
                    item = QSurfaceDataItem((QVector3D(x_plane, y_coord, z_coord)))
                    newRow1.append(item)
                self._flatPlaneDataArray.append(newRow1)

    def addSeries(self):
        for layerSeries in self._layersSeries:
            layerSeries.setDrawMode(QSurface3DSeries.DrawSurface)
            layerSeries.setFlatShadingEnabled(False)
            self._graph.addSeries(layerSeries)
        self._flatPlaneSeries.setDrawMode(QSurface3DSeries.DrawWireframe)
        self._flatPlaneSeries.setFlatShadingEnabled(False)
        self._graph.addSeries(self._flatPlaneSeries)

    def setAxisMultiLayers(self):
        
        self._graph.axisX().setLabelFormat("%.3f")
        self._graph.axisZ().setLabelFormat("%.3f")
        self._graph.axisY().setLabelFormat("%.3f")

        self._graph.axisX().setRange(self._rangeMinX - 0.1, self._rangeMaxX + 0.1)
        self._graph.axisY().setRange(self._rangeMinY, self._rangeMaxY)
        self._graph.axisZ().setRange(self._rangeMinZ - 0.1, self._rangeMaxZ + 0.1)

        self._graph.axisX().setLabelAutoRotation(30.0)
        self._graph.axisY().setLabelAutoRotation(90.0)
        self._graph.axisZ().setLabelAutoRotation(30.0)
        
        self._graph.axisX().setTitleVisible(False)
        self._graph.axisY().setTitleVisible(False)
        self._graph.axisZ().setTitleVisible(False)

        self._graph.axisX().setTitle("")
        self._graph.axisY().setTitle("")
        self._graph.axisZ().setTitle("")

        self._graph.setActiveInputHandler(self._defaultInputHandler)

        self.addSeries()

        self._axisMinSliderX.setMinimum(0)
        self._axisMinSliderX.setMaximum(self._totalStepsX - 2)
        self._axisMinSliderX.setValue(0)
        self._axisMaxSliderX.setMinimum(1)
        self._axisMaxSliderX.setMaximum(self._totalStepsX - 1)
        self._axisMaxSliderX.setValue(self._totalStepsX - 1)

        self._axisMinSliderZ.setMinimum(0)
        self._axisMinSliderZ.setMaximum(self._totalStepsZ - 2)
        self._axisMinSliderZ.setValue(0)
        self._axisMaxSliderZ.setMinimum(1)
        self._axisMaxSliderZ.setMaximum(self._totalStepsZ - 1)
        self._axisMaxSliderZ.setValue(self._totalStepsZ - 1)

        self._flatPlaneSlider.setMinimum(0)#-self._totalStepsX / 2 + 1 if self._rangeMinX < 0 else 1)
        self._flatPlaneSlider.setMaximum(self._totalStepsX - 1)#self._totalStepsX/2 - 1 if self._rangeMinX < 0 else self._totalStepsX - 1)
        self._flatPlaneSlider.setValue(float(self._totalStepsX/2))#0 if self._rangeMinX < 0 else float(self._totalStepsX/2))#float(self._totalStepsZ/2))
        self._flatPlaneSlider.setPageStep(3)

        self._axisMinSliderY.setMinimum(0)
        self._axisMinSliderY.setMaximum(self._totalStepsY - 2)
        self._axisMaxSliderY.setMinimum(1)
        self._axisMaxSliderY.setMaximum(self._totalStepsY - 1)
        self._axisMinSliderY.setValue(0)
        self._axisMaxSliderY.setValue(self._totalStepsY - 1)

    def adjustXMin(self, min):
        minX = self._stepX * float(min) + self._rangeMinX

        max = self._axisMaxSliderX.value()
        if min >= max:
            max = min + 1
            self._axisMaxSliderX.setValue(max)

        maxX = self._stepX * max + self._rangeMinX

        self.setAxisXRange(minX, maxX)

    def adjustXMax(self, max):
        maxX = self._stepX * float(max) + self._rangeMinX

        min = self._axisMinSliderX.value()
        if max <= min:
            min = max - 1
            self._axisMinSliderX.setValue(min)

        minX = self._stepX * min + self._rangeMinX

        self.setAxisXRange(minX, maxX)

    def adjustZMin(self, min):
        minZ = self._stepZ * float(min) + self._rangeMinZ

        max = self._axisMaxSliderZ.value()
        if min >= max:
            max = min + 1
            self._axisMaxSliderZ.setValue(max)

        maxZ = self._stepZ * max + self._rangeMinZ

        self.setAxisZRange(minZ, maxZ)

    def adjustZMax(self, max):
        maxZ = self._stepZ * float(max) + self._rangeMinZ

        min = self._axisMinSliderZ.value()
        if max <= min:
            min = max - 1
            self._axisMinSliderZ.setValue(min)

        minZ = self._stepZ * min + self._rangeMinZ

        self.setAxisZRange(minZ, maxZ)
    
    def adjustYMin(self, min):
        minY = self._stepY * float(min) + self._rangeMinY

        max = self._axisMaxSliderY.value()
        if min >= max:
            max = min + 1
            self._axisMaxSliderY.setValue(max)

        maxY = self._stepY * max + self._rangeMinY

        self.setAxisYRange(minY, maxY)

    def adjustYMax(self, max):
        maxY = self._stepY * float(max) + self._rangeMinY

        min = self._axisMinSliderY.value()
        if max <= min:
            min = max - 1
            self._axisMinSliderY.setValue(min)

        minY = self._stepY * min + self._rangeMinY

        self.setAxisYRange(minY, maxY)

    def setAxisXRange(self, min, max):
        self._graph.axisX().setRange(min, max)

    def setAxisZRange(self, min, max):
        self._graph.axisZ().setRange(min, max)

    def setAxisYRange(self, min, max):
        self._graph.axisY().setRange(min, max)
        self._flatPLaneProxy.resetArray([])
        self.update_line_position(self._slicingPlaneSelectedValue)       

    def setBlackToYellowGradient(self):
        gr = QLinearGradient()

        gr.setColorAt(0.0, Qt.black)
        gr.setColorAt(0.2, Qt.blue)
        gr.setColorAt(0.4, Qt.cyan)
        gr.setColorAt(0.6, Qt.green)
        gr.setColorAt(0.8, Qt.yellow)
        gr.setColorAt(1.0, Qt.red)

        for layerSeries in self._layersSeries:
            layerSeries.setBaseGradient(gr)
            layerSeries.setColorStyle(Q3DTheme.ColorStyleRangeGradient)

    def setGreenToRedGradient(self):
        gr = QLinearGradient()
        gr.setColorAt(0.0, Qt.darkGreen)
        gr.setColorAt(0.5, Qt.yellow)
        gr.setColorAt(0.8, Qt.red)
        gr.setColorAt(1.0, Qt.darkRed)

        for layerSeries in self._layersSeries:
            layerSeries.setBaseGradient(gr)
            layerSeries.setColorStyle(Q3DTheme.ColorStyleRangeGradient)

    def handleElementSelected(self, type):
        self.resetSelection()
        if type == QAbstract3DGraph.ElementCustomItem:
            item = self._graph.selectedCustomItem()
            text = ""
            if isinstance(item, QCustom3DItem):
                text += "Custom label: "
            else:
                file = item.meshFile().split("/")[-1]
                text += f"{file}: "

            text += str(self._graph.selectedCustomItemIndex())
            self._textField.setText(text)
            self._previouslyAnimatedItem = item
            self._previousScaling = item.scaling()
            self._selectionAnimation.setTargetObject(item)
            self._selectionAnimation.setStartValue(item.scaling())
            self._selectionAnimation.setEndValue(item.scaling() * 1.5)
            self._selectionAnimation.start()
        elif type == QAbstract3DGraph.ElementSeries:
            series = self._graph.selectedSeries()
            if series:
                point = series.selectedPoint()
            if self._selectedAxisForSlicing == 'Z':    
                self._slicingPlaneSelectedValue = self._graph.seriesList()[0].dataProxy().itemAt(point).z()
                self._flatPlaneSlider.setValue(self._slicingPlaneSelectedValue / self._stepZ)
            else :
                self._slicingPlaneSelectedValue = self._graph.seriesList()[0].dataProxy().itemAt(point).x()
                self._flatPlaneSlider.setValue(self._slicingPlaneSelectedValue / self._stepX)

        elif (type.value > QAbstract3DGraph.ElementSeries.value
              and type.value < QAbstract3DGraph.ElementCustomItem.value):
            index = self._graph.selectedLabelIndex()
            text = ""
            if type == QAbstract3DGraph.ElementAxisXLabel:
                text += "Axis X label: "
            elif type == QAbstract3DGraph.ElementAxisYLabel:
                text += "Axis Y label: "
            else:
                text += "Axis Z label: "
            text += str(index)
            self._textField.setText(text)
        else:
            self._textField.setText("Nothing")

    def resetSelection(self):
        self._selectionAnimation.stop()
        if self._previouslyAnimatedItem:
            self._previouslyAnimatedItem.setScaling(self._previousScaling)
        self._previouslyAnimatedItem = None

    def setStatisticsTable(self, table:QTableWidget, cbStatsSelector: QComboBox):
        if self._totalLayers > 1:
            cbStatsSelector.addItems([f'Layer {layer + 1}' for layer in range(self._totalLayers)])
            cbStatsSelector.setCurrentIndex(0)

        self.loadStatisticData(table, 0)

    def loadStatisticData(self, table, layerIndex):
        table.setItem(0, 1, QTableWidgetItem(f"{self._statistics[layerIndex]['size']}"))
        table.setItem(1, 1, QTableWidgetItem(f"{(self._statistics[layerIndex]['y_min']*1000).__round__(4)}"))
        table.setItem(2, 1, QTableWidgetItem(f"{(self._statistics[layerIndex]['y_max']*1000).__round__(4)}"))
        table.setItem(3, 1, QTableWidgetItem(f"{(self._statistics[layerIndex]['y_avg']*1000).__round__(4)}"))
        table.setItem(4, 1, QTableWidgetItem(f"{sqrt(self._statistics[layerIndex]['y_variance']).__round__(4)}"))

    def toggleModeNone(self):
        self._graph.setSelectionMode(QAbstract3DGraph.SelectionNone)

    def toggleModeItem(self):
        self._graph.setSelectionMode(QAbstract3DGraph.SelectionItem)

    def setAxisMinSliderX(self, slider):
        self._axisMinSliderX = slider

    def setAxisMaxSliderX(self, slider):
        self._axisMaxSliderX = slider

    def setAxisMinSliderZ(self, slider):
        self._axisMinSliderZ = slider

    def setAxisMaxSliderZ(self, slider):
        self._axisMaxSliderZ = slider
    
    def setAxisMinSliderY(self, slider):
        self._axisMinSliderY = slider

    def setAxisMaxSliderY(self, slider):
        self._axisMaxSliderY = slider

    def setFlatPlaneSlider(self, slider):
        self._flatPlaneSlider = slider

    def setSelectedAxisForSlicing(self, axis):
        if axis not in ['X', 'Z']: return

        self._selectedAxisForSlicing = axis
        totalSteps = self._totalStepsX if axis == 'X' else self._totalStepsZ
        # negative = self._rangeMinX < 0 if axis == 'X' else self._rangeMinZ < 0
        self._flatPlaneSlider.setMinimum(1)#-totalSteps/2 if negative else 1)
        self._flatPlaneSlider.setMaximum(totalSteps - 1)#totalSteps/2 - 1 if negative else totalSteps - 1)
        self._flatPlaneSlider.setValue(float(totalSteps/2))#0 if negative else float(totalSteps/2))#float(self._totalStepsZ/2))
        self.update_line_position()

    # Function to update the line's position based on the slider value
    def update_line_position(self, value = 0):
        self.fillDataForFlatPlane(value)
        self._flatPLaneProxy.resetArray(self._flatPlaneDataArray)

    def PlotLineGraph(self):
        try:
            plotDatas = [data for data, _ in self._plotDatas]
            self._lineGraph.PlotLineGraph(plotDatas, self._slicingPlaneSelectedValue, self._selectedAxisForSlicing)
        except BaseException as error:
            print('An exception occurred: {}'.format(error))
            QMessageBox.information(self, 
                                    "Plot 2D data error",
                                    f"An exception occurred: {format(error)}'.",
                                    QMessageBox.StandardButton.Ok)

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

    def onFlatPlaneSliderChange(self, value):
        if self._selectedAxisForSlicing == 'Z':
            step = self._stepZ
            rangeMax = self._rangeMaxZ
            rangeMin = self._rangeMinZ
        else: 
            step = self._stepX
            rangeMax = self._rangeMaxX
            rangeMin = self._rangeMinX

        newValue = step * float(value) + rangeMin
        if newValue > rangeMax:
            newValue = rangeMax
        if newValue < rangeMin:
            newValue = rangeMin
        self.update_line_position(newValue)
        self._slicingPlaneSelectedValue = newValue
        format_float = "{:.2f}".format(newValue)
        text = "Selected value: " + format_float
        self._textField.setText(text)
    
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

    def RemoveSeries(self):
        self.ResetDataArray()
        self._surfaceProxies = None
        for series in self._layersSeries:
             self._graph.removeSeries(series) 
        for dataArray in self._dataArrays:
            dataArray.clear()
        self._flatPlaneDataArray.clear()

        # for proxy in self._surfaceProxies:
        #     proxy.deleteLater()
        for series in self._layersSeries:
            series.deleteLater()

        # self._layersSeries = None
        # self._dataArrays = None
        # self._plotDatas = None
        # self._flatPLaneProxy.deleteLater()
        # self._dataArrays.clear()
        # self._flatPlaneDataArray.clear()
        # self._x_axis.deleteLater()
        # self._y_axis.deleteLater()
        # self._z_axis.deleteLater()
        # self.matPlotlibImage.deleteLater()
        # self.surfaceImage.deleteLater()
        # self._selectionAnimation.deleteLater()
        # self._lineGraph = None
        # self._graph = None
        # self._axisMinSliderX = None
        # self._axisMaxSliderX = None
        # self._axisMinSliderZ = None
        # self._axisMaxSliderZ = None
        # self._flatPlaneSlider = None
        
        
        
    
