# Copyright (C) 2023 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

import email
from memory_profiler import profile
from pyparsing import enable_all_warnings

from .surfacegraphmodifier2 import SurfaceGraphModifier
from widgets.scatter_graph.scatterdatamodifier import ScatterDataModifier

from PySide6.QtCore import QObject, Qt, Signal
from PySide6.QtGui import QBrush, QIcon, QLinearGradient, QPainter, QPixmap
from PySide6.QtWidgets import *

from PySide6.QtDataVisualization import Q3DSurface, Q3DScatter
from widgets.mplwidget import MplGraph


def gradientBtoYPB_Pixmap():
    grBtoY = QLinearGradient(0, 0, 1, 100)

    grBtoY.setColorAt(1.0, Qt.black)
    grBtoY.setColorAt(0.8, Qt.blue)
    grBtoY.setColorAt(0.6, Qt.cyan)
    grBtoY.setColorAt(0.4, Qt.green)
    grBtoY.setColorAt(0.2, Qt.yellow)
    grBtoY.setColorAt(0.0, Qt.red)

    pm = QPixmap(24, 100)
    with QPainter(pm) as pmp:
        pmp.setBrush(QBrush(grBtoY))
        pmp.setPen(Qt.NoPen)
        pmp.drawRect(0, 0, 24, 100)
    return pm


def gradientGtoRPB_Pixmap():
    grGtoR = QLinearGradient(0, 0, 1, 100)
    grGtoR.setColorAt(1.0, Qt.black)
    grGtoR.setColorAt(0.8, Qt.darkGreen)
    grGtoR.setColorAt(0.6, Qt.yellow)
    grGtoR.setColorAt(0.4, Qt.red)
    grGtoR.setColorAt(0.2, Qt.darkRed)
    pm = QPixmap(24, 100)
    with QPainter(pm) as pmp:
        pmp.setBrush(QBrush(grGtoR))
        pmp.setPen(Qt.NoPen)
        pmp.drawRect(0, 0, 24, 100)
    return pm


def highlightPixmap():
    HEIGHT = 400
    WIDTH = 110
    BORDER = 10
    gr = QLinearGradient(0, 0, 1, HEIGHT - 2 * BORDER)
    gr.setColorAt(1.0, Qt.black)
    gr.setColorAt(0.8, Qt.darkGreen)
    gr.setColorAt(0.6, Qt.green)
    gr.setColorAt(0.4, Qt.yellow)
    gr.setColorAt(0.2, Qt.red)
    gr.setColorAt(0.0, Qt.darkRed)
    pmHighlight = QPixmap(WIDTH, HEIGHT)
    pmHighlight.fill(Qt.transparent)
    with QPainter(pmHighlight) as pmpHighlight:
        pmpHighlight.setBrush(QBrush(gr))
        pmpHighlight.setPen(Qt.NoPen)
        pmpHighlight.drawRect(BORDER, BORDER, 35, HEIGHT - 2 * BORDER)
        pmpHighlight.setPen(Qt.black)
        step = (HEIGHT - 2 * BORDER) / 5
        for i in range(0, 6):
            yPos = i * step + BORDER
            pmpHighlight.drawLine(BORDER, yPos, 55, yPos)
            HEIGHT = 550 - (i * 110)
            pmpHighlight.drawText(60, yPos + 2, f"{HEIGHT} m")
    return pmHighlight


class SurfaceGraph(QObject):
    graphImagesChanged = Signal(str)
    def __init__(self, graphName:str, dataFrames, layerParams):
        super().__init__()
        self._surfaceGraph = Q3DSurface()
        self._container = None
        self._surfaceWidget = None
        self._modifier = None
        self._graphName = graphName
        self._dataFrames = dataFrames
        self._layerParams = layerParams

    def initialize(self, minimum_graph_size, maximum_graph_size):
        if not self._surfaceGraph.hasContext():
            return False

        self._surfaceWidget = QWidget()
        self._surfaceGraph.setTitle("Surface graph")
        self._lineGraph = MplGraph(self._surfaceWidget)
        self._lineGraph.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        hLayout = QHBoxLayout(self._surfaceWidget)
        self._container = QWidget.createWindowContainer(self._surfaceGraph,
                                                        self._surfaceWidget)
        self._container.setMinimumSize(minimum_graph_size)
        #self._container.setMaximumSize(maximum_graph_size)
        self._container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._container.setFocusPolicy(Qt.StrongFocus)


        splitter = QSplitter(Qt.Orientation.Horizontal, parent=self._surfaceWidget)
        splitter.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        splitter.setFocusPolicy(Qt.StrongFocus)
        splitter.setContentsMargins(0, 0, 0, 0)
        splitter.addWidget(self._container)
        splitter.addWidget(self._lineGraph)

        hLayout.addWidget(splitter, 1)
        # hLayout.addWidget(self._container, 1)
        # hLayout.addWidget(self._lineGraph)

        vLayout = QVBoxLayout()
        vLayout.setAlignment(Qt.AlignTop)

        vlayoutContainer = QScrollArea()
        vlayoutContainer.setFixedWidth(200)
        vlayoutContainer.setLayout(vLayout)

        hLayout.addWidget(vlayoutContainer)

        # Create control widgets

        graphEnableGroupBox = QGroupBox("Show graph")
        enableSurface = QCheckBox(self._surfaceWidget)
        enableSurface.setText("Surface Graph")
        enableSurface.setChecked(True)
        enable2dSliced = QCheckBox(self._surfaceWidget)
        enable2dSliced.setText("2D Graph")
        enable2dSliced.setChecked(True)
        graphEnableGroupBoxLayout = QVBoxLayout()
        graphEnableGroupBoxLayout.addWidget(enableSurface)
        graphEnableGroupBoxLayout.addWidget(enable2dSliced)
        graphEnableGroupBox.setLayout(graphEnableGroupBoxLayout)

        selectionGroupBox = QGroupBox("Graph Mode Selection")
        modeNoneRB = QRadioButton(self._surfaceWidget)
        modeNoneRB.setText("No selection")
        modeNoneRB.setChecked(False)
        modeItemRB = QRadioButton(self._surfaceWidget)
        modeItemRB.setText("Item")
        modeItemRB.setChecked(False)
        modeOrthogonal = QCheckBox(self._surfaceWidget)
        modeOrthogonal.setText("Orthogonal Projection")
        modeOrthogonal.setChecked(False)
        selectionVBox = QVBoxLayout()
        selectionVBox.addWidget(modeNoneRB)
        selectionVBox.addWidget(modeItemRB)
        selectionVBox.addWidget(modeOrthogonal)
        selectionGroupBox.setLayout(selectionVBox)

        selectionSliceAxisGB = QGroupBox("2D Graph Axis Selection")
        rowRB = QRadioButton(self._surfaceWidget)
        rowRB.setText("X Axis")
        rowRB.setChecked(True)
        columnRB = QRadioButton(self._surfaceWidget)
        columnRB.setText("Y Axis")
        columnRB.setChecked(False)
        selectionSliceAxisLayout = QVBoxLayout()
        selectionSliceAxisLayout.addWidget(rowRB)
        selectionSliceAxisLayout.addWidget(columnRB)
        selectionSliceAxisGB.setLayout(selectionSliceAxisLayout)

        axisGroupBox = QGroupBox("Axis ranges")
        axisMinSliderX = QSlider(Qt.Horizontal)
        axisMinSliderX.setMinimum(0)
        axisMinSliderX.setTickInterval(1)
        axisMinSliderX.setEnabled(True)
        axisMaxSliderX = QSlider(Qt.Horizontal)
        axisMaxSliderX.setMinimum(1)
        axisMaxSliderX.setTickInterval(1)
        axisMaxSliderX.setEnabled(True)
        axisMinSliderZ = QSlider(Qt.Horizontal)
        axisMinSliderZ.setMinimum(0)
        axisMinSliderZ.setTickInterval(1)
        axisMinSliderZ.setEnabled(True)
        axisMaxSliderZ = QSlider(Qt.Horizontal)
        axisMaxSliderZ.setMinimum(1)
        axisMaxSliderZ.setTickInterval(1)
        axisMaxSliderZ.setEnabled(True)
        axisMinSliderY = QSlider(Qt.Horizontal)
        axisMinSliderY.setMinimum(0)
        axisMinSliderY.setTickInterval(1)
        axisMinSliderY.setEnabled(True)
        axisMaxSliderY = QSlider(Qt.Horizontal)
        axisMaxSliderY.setMinimum(1)
        axisMaxSliderY.setTickInterval(1)
        axisMaxSliderY.setEnabled(True)
        flatPlaneSlider = QSlider(Qt.Horizontal)
        flatPlaneSlider.setFixedWidth(100)
        flatPlaneSlider.setMinimum(1)
        flatPlaneSlider.setTickInterval(1)
        flatPlaneSlider.setEnabled(True)
        axisVBox = QVBoxLayout(axisGroupBox)
        axisVBox.addWidget(QLabel("Column range"))
        axisVBox.addWidget(axisMinSliderX)
        axisVBox.addWidget(axisMaxSliderX)
        axisVBox.addWidget(QLabel("Row range"))
        axisVBox.addWidget(axisMinSliderZ)
        axisVBox.addWidget(axisMaxSliderZ)
        axisVBox.addWidget(QLabel("Weight range"))
        axisVBox.addWidget(axisMinSliderY)
        axisVBox.addWidget(axisMaxSliderY)
        # Mode-dependent controls
        colorGroupBox = QGroupBox("Custom gradient")

        pixmap = gradientBtoYPB_Pixmap()
        gradientBtoYPB = QPushButton(self._surfaceWidget)
        gradientBtoYPB.setIcon(QIcon(pixmap))
        gradientBtoYPB.setIconSize(pixmap.size())

        pixmap = gradientGtoRPB_Pixmap()
        gradientGtoRPB = QPushButton(self._surfaceWidget)
        gradientGtoRPB.setIcon(QIcon(pixmap))
        gradientGtoRPB.setIconSize(pixmap.size())

        colorHBox = QHBoxLayout(colorGroupBox)
        colorHBox.addWidget(gradientBtoYPB)
        colorHBox.addWidget(gradientGtoRPB)
 
        labelSelectedItem = QLabel("Nothing")
        labelSelectedItem.setVisible(True)

        label = QLabel(self._surfaceWidget)
        label.setPixmap(highlightPixmap())
        heightMapGroupBox = QGroupBox("Highlight color map")
        colorMapVBox = QVBoxLayout()
        colorMapVBox.addWidget(label)
        heightMapGroupBox.setLayout(colorMapVBox)
        heightMapGroupBox.setVisible(False)

        plotButton = QPushButton(text="Plot 2D", parent=self._surfaceWidget)
        plotButton.setFixedSize(60, 40)
        slideUpButton = QPushButton(text="+", parent=self._surfaceWidget)
        slideUpButton.setFixedSize(30,30)
        slideDownButton = QPushButton(text="-", parent=self._surfaceWidget)
        slideDownButton.setFixedSize(30,30)
        hPlaneSliderLayout = QHBoxLayout()
        hPlaneSliderLayout.addWidget(slideDownButton)
        hPlaneSliderLayout.addWidget(flatPlaneSlider)
        hPlaneSliderLayout.addWidget(slideUpButton)

        lockImageButton = QPushButton(text="Set graph image", parent=self._surfaceWidget)
        lockImageButton.setFixedSize(100, 40)

        statisticsTable = QTableWidget(self._surfaceWidget)
        statisticsTable.setObjectName("Layer Statistics")
        statisticsTable.setRowCount(5)
        statisticsTable.setColumnCount(2)
        statisticsTable.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        statisticsTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        statisticsTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        statisticsTable.setHorizontalHeaderLabels(["", "Value(um)"])
        statisticsTable.setItem(0, 0, QTableWidgetItem("Population size"))
        statisticsTable.setItem(1, 0, QTableWidgetItem("Min"))
        statisticsTable.setItem(2, 0, QTableWidgetItem("Max"))
        statisticsTable.setItem(3, 0, QTableWidgetItem("Mean"))
        statisticsTable.setItem(4, 0, QTableWidgetItem("Standard Deviation"))

        cbSelectLayerForStats = QComboBox(self._surfaceWidget)
        cbSelectLayerForStats.setObjectName("Layer stats selector")
        cbSelectLayerForStats.setCurrentText("Single layer")
        cbSelectLayerForStats.setPlaceholderText("Select layer")
        cbSelectLayerForStats.currentIndexChanged.connect(lambda index: self._modifier.loadStatisticData(statisticsTable, index))

        # Populate vertical layout
        vLayout.addWidget(graphEnableGroupBox)
        vLayout.addWidget(selectionGroupBox)
        vLayout.addWidget(selectionSliceAxisGB)
        vLayout.addWidget(axisGroupBox)
        vLayout.addWidget(colorGroupBox)
        vLayout.addWidget(labelSelectedItem)
        vLayout.addLayout(hPlaneSliderLayout)
        vLayout.addWidget(plotButton)   
        vLayout.addWidget(lockImageButton)
        vLayout.addWidget(cbSelectLayerForStats)
        vLayout.addWidget(statisticsTable)


        # Create the controller
        self._modifier = SurfaceGraphModifier(self._surfaceGraph, labelSelectedItem, self._lineGraph, self, self._dataFrames, self._layerParams)

        #Connect graph enable buttons
        enableSurface.stateChanged.connect(lambda state: self._container.setVisible(state))
        enable2dSliced.stateChanged.connect(lambda state: self._lineGraph.setVisible(state))
        
        # Connect widget controls to controller
        modeNoneRB.toggled.connect(self._modifier.toggleModeNone)
        modeItemRB.toggled.connect(self._modifier.toggleModeItem)
        modeOrthogonal.toggled.connect(self._modifier.OrthogonalProjection)

        axisMinSliderX.valueChanged.connect(self._modifier.adjustXMin)
        axisMaxSliderX.valueChanged.connect(self._modifier.adjustXMax)
        axisMinSliderZ.valueChanged.connect(self._modifier.adjustZMin)
        axisMaxSliderZ.valueChanged.connect(self._modifier.adjustZMax)
        axisMinSliderY.valueChanged.connect(self._modifier.adjustYMin)
        axisMaxSliderY.valueChanged.connect(self._modifier.adjustYMax)

        # Mode dependent connections
        gradientBtoYPB.pressed.connect(self._modifier.setBlackToYellowGradient)
        gradientGtoRPB.pressed.connect(self._modifier.setGreenToRedGradient)

        # Connections to disable features depending on mode
        self._modifier.setAxisMinSliderX(axisMinSliderX)
        self._modifier.setAxisMaxSliderX(axisMaxSliderX)
        self._modifier.setAxisMinSliderZ(axisMinSliderZ)
        self._modifier.setAxisMaxSliderZ(axisMaxSliderZ)
        self._modifier.setAxisMinSliderY(axisMinSliderY)
        self._modifier.setAxisMaxSliderY(axisMaxSliderY)
        self._modifier.setFlatPlaneSlider(flatPlaneSlider)
        modeItemRB.setChecked(True)

        plotButton.clicked.connect(self._modifier.PlotLineGraph)
        lockImageButton.clicked.connect(self.RenderGraphImages)
        flatPlaneSlider.valueChanged.connect(self._modifier.onFlatPlaneSliderChange)
        slideUpButton.clicked.connect(self._modifier.SlideUpOne)
        slideDownButton.clicked.connect(self._modifier.SlideDownOne)

        rowRB.clicked.connect(lambda: self._modifier.setSelectedAxisForSlicing('X'))
        columnRB.clicked.connect(lambda: self._modifier.setSelectedAxisForSlicing('Z'))

        return True

    def surfaceWidget(self):
        return self._surfaceWidget
    
    def AddData(self):
        self._modifier.fillMultiLayerData()
        self._modifier.setStatisticsTable(self._surfaceWidget.findChild(QTableWidget, "Layer Statistics"),
                                          self._surfaceWidget.findChild(QComboBox,"Layer stats selector"))

    def ResetData(self):
        self._modifier.ResetDataArray()

    def EnableGraph(self):
        self._modifier.setAxisMultiLayers()

    def SetGraphProxies(self):
        self._modifier.SetProxiesArray()

    def RenderGraphImages(self):
        try:
            self._modifier.RenderGraphImages(self._graphName)
            self.graphImagesChanged.emit(self._graphName)
        except BaseException as error:
            print('An exception occurred: {}'.format(error))
            QMessageBox.information(None, 
                                    "Image render error",
                                    f"An exception occurred: {format(error)}'.",
                                    QMessageBox.StandardButton.Ok)


    def GetSurfaceGraphImage(self):
        return self._modifier.surfaceImage
    
    def GetMatplotlibGraphImage(self):
        return self._modifier.matPlotlibImage
    
    def ViewDetail(self):
        self._modifier.SetProxiesArray()
        self._modifier.setAxisMultiLayers()
        self._surfaceWidget.showMaximized()

    def RemoveDataSeries(self):
        self._modifier.RemoveSeries()
        self._surfaceWidget.deleteLater()
        self._container.deleteLater()
        self._surfaceGraph.deleteLater()
        self._lineGraph.deleteLater()
        self._modifier.deleteLater()
        self._surfaceGraph.destroy()
        self._dataFrames = None

    


    
    
    
