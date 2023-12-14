# Copyright (C) 2023 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

from PySide6.QtCore import QObject, QSize, Qt
from PySide6.QtWidgets import *
from PySide6.QtDataVisualization import (QAbstract3DSeries, Q3DScatter)

from .scatterdatamodifier import ScatterDataModifier
from widgets.mplwidget import MplGraph


class ScatterGraph(QObject):

    def __init__(self, graphName:str, dataFrames):
        super().__init__()
        self._scatterGraph = Q3DScatter()
        self._lineGraph = None
        self._container = None
        self._scatterWidget = None
        self._graphName = graphName
        self._dataFrames = dataFrames

    def initialize(self, minimum_graph_size, maximum_graph_size):
        if not self._scatterGraph.hasContext():
            return -1

        self._scatterWidget = QWidget()
        self._lineGraph = MplGraph(self._scatterWidget)
        self._lineGraph.setMinimumWidth(600)
        self._lineGraph.setMinimumHeight(300)
        self._lineGraph.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        hLayout = QHBoxLayout(self._scatterWidget)
        self._container = QWidget.createWindowContainer(self._scatterGraph, self._scatterWidget)
        self._container.setMinimumSize(minimum_graph_size)
        self._container.setMaximumSize(maximum_graph_size)
        self._container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._container.setFocusPolicy(Qt.StrongFocus)
        hLayout.addWidget(self._container)
        hLayout.addWidget(self._lineGraph)

        vLayout = QVBoxLayout()
        hLayout.addLayout(vLayout)

        cameraButton = QCommandLinkButton(self._scatterWidget)
        cameraButton.setText("Change camera preset")
        cameraButton.setDescription("Switch between a number of preset camera positions")
        cameraButton.setIconSize(QSize(0, 0))

        itemStyleList = QComboBox(self._scatterWidget)
        itemStyleList.addItem("Sphere", QAbstract3DSeries.MeshSphere)
        itemStyleList.addItem("Cube", QAbstract3DSeries.MeshCube)
        itemStyleList.addItem("Minimal", QAbstract3DSeries.MeshMinimal)
        itemStyleList.addItem("Point", QAbstract3DSeries.MeshPoint)
        itemStyleList.setCurrentIndex(3)

        selectionGroupBox = QGroupBox("Graph Selection Mode")
        modeNoneRB = QRadioButton(self._scatterWidget)
        modeNoneRB.setText("No selection")
        modeNoneRB.setChecked(False)
        modeItemRB = QRadioButton(self._scatterWidget)
        modeItemRB.setText("Item")
        modeItemRB.setChecked(False)
        modeSliceRowRB = QRadioButton(self._scatterWidget)
        modeSliceRowRB.setText("Row Slice")
        modeSliceRowRB.setChecked(False)
        modeSliceColumnRB = QRadioButton(self._scatterWidget)
        modeSliceColumnRB.setText("Column Slice")
        modeSliceColumnRB.setChecked(False)
        selectionVBox = QVBoxLayout()
        selectionVBox.addWidget(modeNoneRB)
        selectionVBox.addWidget(modeItemRB)
        selectionVBox.addWidget(modeSliceRowRB)
        selectionVBox.addWidget(modeSliceColumnRB)
        selectionGroupBox.setLayout(selectionVBox)

        themeList = QComboBox(self._scatterWidget)
        themeList.addItem("Qt")
        themeList.addItem("Primary Colors")
        themeList.addItem("Digia")
        themeList.addItem("Stone Moss")
        themeList.addItem("Army Blue")
        themeList.addItem("Retro")
        themeList.addItem("Ebony")
        themeList.addItem("Isabelle")
        themeList.setCurrentIndex(0)

        vLayout.addWidget(selectionGroupBox)
        vLayout.addWidget(cameraButton)
        vLayout.addWidget(QLabel("Change dot style"))
        vLayout.addWidget(itemStyleList)
        vLayout.addWidget(QLabel("Change theme"))
        vLayout.addWidget(themeList)

        self._modifier = ScatterDataModifier(self._scatterGraph, self._lineGraph, self, self._dataFrames)
        vLayout.addWidget(self._modifier.label, alignment=Qt.AlignmentFlag.AlignTop)
        
        cameraButton.clicked.connect(self._modifier.changePresetCamera)

        itemStyleList.currentIndexChanged.connect(self._modifier.changeStyle)

        themeList.currentIndexChanged.connect(self._modifier.changeTheme)


        modeNoneRB.toggled.connect(self._modifier.toggleModeNone)
        modeItemRB.toggled.connect(self._modifier.toggleModeItem)
        modeSliceRowRB.toggled.connect(self._modifier.toggleModeSliceRow)
        modeSliceColumnRB.toggled.connect(self._modifier.toggleModeSliceColumn)
        return True

    def scatterWidget(self):
        return self._scatterWidget
    
    def AddData(self, plotData):
        self._modifier.SetPlotData(plotData)
        
    
