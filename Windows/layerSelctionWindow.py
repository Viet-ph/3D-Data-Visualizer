import os
import numpy as np
# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtDataVisualization import *
from modules.gui_modules.ui_layerSelection import Ui_LayerSelection
from modules.gui_modules.app_settings import Settings
from modules.gui_modules.ui_functions import UIFunctions

os.environ["QT_FONT_DPI"] = "96" # FIX Problem for High DPI and Scale above 100%

# SET AS GLOBAL WIDGETS
# ///////////////////////////////////////////////////////////////
widgets = None
GLOBAL_STATE = False


class LayerSelectionWindow(QMainWindow):
    dataSubmitted = Signal(list)

    def __init__(self, layerCatagories: list, plotDatas: dict):
        super().__init__()
        
        self.layerCategories = layerCatagories
        self.SingleSetected = True
        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_LayerSelection()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui
        self.plotDatas = plotDatas
        self.layerParams = None
        self.layerTables = [None, widgets.tableLayer1, widgets.tableLayer2, widgets.tableLayer3, widgets.tableLayer4]
        self.selectedLayersList = []

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = "Select layer"

        # APPLY TEXTS
        self.setWindowTitle(title)

        # SET UI DEFINITIONS
        #STANDARD TITLE BAR
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # MOVE WINDOW / MAXIMIZE / RESTORE
        def moveWindow(event):
            # IF MAXIMIZED CHANGE TO NORMAL
            if UIFunctions.returStatus():
                UIFunctions.maximize_restore(self)
            # MOVE WINDOW
            if event.buttons() == Qt.LeftButton:
                delta = QPoint((event.globalPosition() - self.dragPos).x(), (event.globalPosition() - self.dragPos).y())
                self.move(self.pos() + delta)
                self.dragPos = event.globalPos()
                event.accept()
        self.ui.contentTopBg.mouseMoveEvent = moveWindow

        # DROP SHADOW
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(17)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 150))
        self.ui.bgApp.setGraphicsEffect(self.shadow)

        # RESIZE WINDOW
        self.sizegrip = QSizeGrip(self.ui.frame_size_grip)
        self.sizegrip.setStyleSheet("width: 20px; height: 20px; margin 0px; padding: 0px;")

        # MINIMIZE
        self.ui.minimizeAppBtn.clicked.connect(lambda: self.showMinimized())

        # MAXIMIZE/RESTORE
        self.ui.maximizeRestoreAppBtn.clicked.connect(self.maximize_restore)

        # CLOSE APPLICATION
        self.ui.closeAppBtn.clicked.connect(lambda: self.close())

        # QTableWidget PARAMETERS
        # ///////////////////////////////////////////////////////////////
        widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////
        widgets.btnSelect.clicked.connect(self.ConfirmData)
        widgets.btnBack.clicked.connect(self.BackToLayerSelectionPage)

        # LEFT MENUS
        widgets.btn_singleLayer.clicked.connect(self.ButtonCliked)
        widgets.btn_multiLayers.clicked.connect(self.ButtonCliked)

        #LAYER PARAMETERS CHANGED
        widgets.leThicknessValue.textChanged.connect(self.OnThicknessChanged)
        widgets.sbUpperTolerance.valueChanged.connect(self.OnUpperTolChanged)
        widgets.spLowerTolerance.valueChanged.connect(self.OnLowerTolChanged)
        widgets.rbMicro.toggled.connect(self.OnMicroSelected)

        # SET DEFAULT SINGLE LAYER SELECTION
        # ///////////////////////////////////////////////////////////////
        self.BackToLayerSelectionPage()
        widgets.btn_singleLayer.setStyleSheet(UIFunctions.selectMenu(widgets.btn_singleLayer.styleSheet()))

        widgets.tabLayers.tabBar().setStyleSheet(
            """
            QTabBar::tab {
                color: #f2ebf2;
                background-color: #211921;
                }
            QTabBar::tab:selected {
                color: #0f0d0f;
                background-color: #ba7db7;
                }
                                                 
            """)
        
        table = widgets.tableWidget
        table.setColumnCount(2)
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Custom)
        table.horizontalHeader().setDefaultSectionSize(200)
        table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setSelectionMode(QAbstractItemView.SingleSelection)
        table.setHorizontalHeaderLabels(["File names", "Layer index"])
        table.itemPressed.connect(self.OnTableCellWidgetClicked)

        selectedLayersTable = widgets.selectedLayers
        selectedLayersTable.setColumnCount(2)
        selectedLayersTable.setFixedHeight(300)
        selectedLayersTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Custom)
        selectedLayersTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        selectedLayersTable.horizontalHeader().setDefaultSectionSize(200)
        selectedLayersTable.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        selectedLayersTable.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        selectedLayersTable.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        selectedLayersTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        selectedLayersTable.setSelectionMode(QAbstractItemView.SingleSelection)
        selectedLayersTable.setHorizontalHeaderLabels(["Layers", "Selected datas"])

        for i in range(4):
            selectedLayersTable.insertRow(i)
            selectedLayersTable.setCellWidget(i, 0, QLabel("Layer " + str(i + 1)))
            selectedLayersTable.setColumnWidth(0, 200)

        for table in self.layerTables[1:]:
            table.setColumnCount(1)
            table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
            table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Custom)
            table.horizontalHeader().setDefaultSectionSize(200)
            table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            table.setSelectionBehavior(QAbstractItemView.SelectRows)
            table.setSelectionMode(QAbstractItemView.SingleSelection)
            table.setHorizontalHeaderLabels(["Loaded data"])

        self.SetSingleLayerContent()
        self.SetMultiLayersContent()
        self.ui.label.setText(f"{len(self.selectedLayersList)} layer selected")

        
    def ButtonCliked(self):
        btn = self.sender()
        btnName = btn.objectName()
        widgets = self.ui

        # SHOW SINGLE LAYER PAGE
        if btnName == "btn_singleLayer":
            self.SingleSetected = True
            self.BackToLayerSelectionPage()
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))
            self.selectedLayersList.clear()
            self.ui.label.setText(f"{len(self.selectedLayersList)} layer selected")

        # SHOW MULTI LAYERS PAGE
        if btnName == "btn_multiLayers":
            self.SingleSetected = False
            widgets.stackedWidget.setCurrentWidget(widgets.MultiLayers)
            widgets.tabLayers.setCurrentWidget(widgets.Layer1)
            widgets.btnSelect.setText("Render Graph")
            widgets.btnSelect.setIcon(QIcon())
            widgets.btnBack.setVisible(False)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))
            self.selectedLayersList.clear()
            self.ui.label.setText(f"{len(self.selectedLayersList)} layer selected")

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPosition()

        # PRINT MOUSE EVENTS
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICKED')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICKED')

    def maximize_restore(mainWindow):
        global GLOBAL_STATE
        status = GLOBAL_STATE
        if status == False:
            mainWindow.showMaximized()
            GLOBAL_STATE = True
            mainWindow.ui.maximizeRestoreAppBtn.setToolTip("Restore")
            mainWindow.ui.maximizeRestoreAppBtn.setIcon(QIcon(u":/icons/images/icons/icon_restore.png"))
            mainWindow.ui.frame_size_grip.hide()
        else:
            GLOBAL_STATE = False
            mainWindow.showNormal()
            mainWindow.resize(mainWindow.width()+1, mainWindow.height()+1)
            mainWindow.ui.maximizeRestoreAppBtn.setToolTip("Maximize")
            mainWindow.ui.maximizeRestoreAppBtn.setIcon(QIcon(u":/icons/images/icons/icon_maximize.png"))
            mainWindow.ui.frame_size_grip.show()

    # def closeEvent(self, event):
    #     folder_path = 'PlotImages'

    #     for root, dirs, files in os.walk(folder_path):
    #         for file in files:
    #             if file.endswith('.png') or file.endswith('.html'):
    #                 os.remove(os.path.join(root, file))

    def OnTableCellWidgetClicked(self, item: QTableWidgetItem):
        self.ui.label.setText("1 layer selected: " + item.text())
        self.selectedLayersList.clear()
        self.selectedLayersList.append(item.text())
        

    def SetSingleLayerContent(self):
        table = self.ui.tableWidget
        for layer in self.layerCategories:
            for item in layer:
                rowPosition = table.rowCount()
                layerIndex =  self.layerCategories.index(layer)
                string = ("Layer " + str(layerIndex)) if layerIndex != 0 else "None" 
                table.insertRow(rowPosition)
                table.setItem(rowPosition, 0, QTableWidgetItem(item))
                table.setItem(rowPosition, 1, QTableWidgetItem(string))

    def SetMultiLayersContent(self):
        index = 1
        for layer in self.layerCategories[1:]:
            if len(layer) != 0:
                table = self.layerTables[index]
                for item in layer:
                    hlayout = QHBoxLayout()
                    cellWidget = QWidget()
                    addButton = QPushButton("Add")
                    addButton.clicked.connect(self.OnLayerAdded)
                    addButton.setFixedSize(80, 35)
                    addButton.setStyleSheet(
                        """
                        QPushButton{
                            background-color: #4CAF50; 
                            border-radius: 6px;
                            border: none; 
                            color: white;
                            padding: 5px 15px; 
                            text-align: center; 
                            text-decoration: none;
                            display: inline-block;
                            font-size: 13px;
                        }

                        QPushButton:hover{
                            background-color: #a3e3b4;
                            color: black;
                        }           
                        """
                    )
                    hlayout.addWidget(QLabel(item))
                    hlayout.addWidget(addButton)
                    cellWidget.setLayout(hlayout)

                    row_position = table.rowCount()
                    table.insertRow(row_position)
                    table.setCellWidget(row_position, 0, cellWidget)
                    table.resizeRowsToContents()
            index += 1

    def OnLayerAdded(self):
        widget = self.sender().parent()
        print(widget)
        tableIndex = self.ui.tabLayers.currentIndex()
        if(type(self.ui.selectedLayers.cellWidget(tableIndex, 1)) != type(None)):
           QMessageBox.information(self, "Warning", 
                                   "This layer already have data. Remove data first before select others", 
                                   QMessageBox.StandardButton.Ok)
           return
        table = self.layerTables[tableIndex + 1]

        
        preAddRowNumber = table.rowAt(widget.pos().y())
        table.removeRow(preAddRowNumber)
        
        cellWidget = QWidget()
        hlayout = QHBoxLayout(cellWidget)
        removeButton = QPushButton("Remove")
        removeButton.setFixedSize(100, 35)
        removeButton.setStyleSheet(
            """
            QPushButton{
                background-color: #e01d16; 
                border-radius: 6px;
                border: none; 
                color: white;
                padding: 5px 15px; 
                text-align: center; 
                text-decoration: none;
                display: inline-block;
                font-size: 13px;
            }

            QPushButton:hover{
                background-color: #e68d8a;
                color: black;
            }           
            """
        )
        removeButton.clicked.connect(self.OnLayerRemoved)
        label = widget.children()[1]
        hlayout.addWidget(label)
        hlayout.addWidget(removeButton)
        self.ui.selectedLayers.setCellWidget(tableIndex, 1, cellWidget)
        self.ui.selectedLayers.resizeRowsToContents()
        self.selectedLayersList.append(label.text())
        #print(self.selectedLayersList)
        self.ui.label.setText(f"{len(self.selectedLayersList)} layers selected")
        
    def OnLayerRemoved(self):
        widget = self.sender().parent()
        print(widget)
        selectedLayersTable = self.ui.selectedLayers
        dataRowToRemove = selectedLayersTable.rowAt(widget.pos().y())

        #Get table to re-add the data
        table = self.layerTables[dataRowToRemove + 1]
        
        selectedLayersTable.removeCellWidget(dataRowToRemove, 1)
        
        hlayout = QHBoxLayout()
        cellWidget = QWidget()
        addButton = QPushButton("Add")
        addButton.clicked.connect(self.OnLayerAdded)
        addButton.setFixedSize(80, 35)
        addButton.setStyleSheet(
            """
            QPushButton{
                background-color: #4CAF50; 
                border-radius: 6px;
                border: none; 
                color: white;
                padding: 5px 15px; 
                text-align: center; 
                text-decoration: none;
                display: inline-block;
                font-size: 13px;
            }

            QPushButton:hover{
                background-color: #a3e3b4;
                color: black;
            }           
            """
        )
        label = widget.children()[1]
        hlayout.addWidget(label)
        hlayout.addWidget(addButton)
        cellWidget.setLayout(hlayout)
        row_position = table.rowCount()
        table.insertRow(row_position)
        table.setCellWidget(row_position, 0, cellWidget)
        table.resizeRowsToContents()
        self.selectedLayersList.remove(label.text())
        print(self.selectedLayersList)
        self.ui.label.setText(f"{len(self.selectedLayersList)} layers selected")
    
    def BackToLayerSelectionPage(self):
        widgets = self.ui
        widgets.stackedWidget.setCurrentWidget(widgets.SingleLayer)
        widgets.btnBack.setVisible(False)
        widgets.btnSelect.setText("Next")
        widgets.btnSelect.setIcon(QIcon(":/icons/images/icons/cil-arrow-circle-right.png"))

    def LoadSettingParamsPage(self, dataFileName: str):
        widgets = self.ui
        _, statistics = self.plotDatas[dataFileName]
        y_avg = statistics['y_avg']
        y_max = statistics['y_max']
        y_min = statistics['y_min']
        widgets.leThicknessValue.setText(str(y_avg.__round__(4)))
        widgets.spLowerTolerance.setValue((y_avg - y_min).__round__(4))
        widgets.sbUpperTolerance.setValue((y_max - y_avg).__round__(4))

    def SetLayerParams(self):
        widgets = self.ui
        self.layerParams = dict(thickness = float(widgets.leThicknessReadOnly.text()), 
                                upperLimit = float(widgets.leUpperLimitReadOnly.text()),
                                lowerLimit = float(widgets.leLowerLimitReadOnly.text()))

    def ConfirmData(self):
        btn = self.sender()
        widgets = self.ui
        if (len(self.selectedLayersList) == 0):
            QMessageBox.warning(self, 
                                "Warning", 
                                "Select at least 1 layer to plot.", 
                                QMessageBox.StandardButton.Ok)
            return
        if (len(self.selectedLayersList) == 1 and self.SingleSetected == False):
            QMessageBox.information(self, 
                                "Render multilayers", 
                                "Only 1 layer selected. Choose single layer instead.", 
                                QMessageBox.StandardButton.Ok)
            return
        if btn.text() == "Render Graph":
            self.close()
            widgets.rbMilli.toggle()
            if self.SingleSetected:
                self.SetLayerParams()
                self.dataSubmitted.emit((self.selectedLayersList, self.layerParams))
            else:
                self.dataSubmitted.emit((self.selectedLayersList, None))

        else:
            btn.setText("Render Graph")
            btn.setIcon(QIcon())
            widgets.btnBack.setVisible(True)
            self.LoadSettingParamsPage(self.selectedLayersList[0])
            widgets.stackedWidget.setCurrentWidget(widgets.SettingParams)
        
    def OnThicknessChanged(self, value):
        widgets = self.ui
        newThickness = float(value)
        newUpperLimit = newThickness + widgets.sbUpperTolerance.value()
        newLowerLimit = newThickness - widgets.spLowerTolerance.value()
        widgets.leThicknessReadOnly.setText(str(newThickness.__round__(4)))
        widgets.leUpperLimitReadOnly.setText(str(newUpperLimit.__round__(4)))
        widgets.leLowerLimitReadOnly.setText(str(newLowerLimit.__round__(4)))

    def OnUpperTolChanged(self, value):
        widgets = self.ui
        thickness = float(widgets.leThicknessReadOnly.text())
        newUpperLimit = thickness + value
        widgets.leUpperLimitReadOnly.setText(str(newUpperLimit.__round__(4)))

    def OnLowerTolChanged(self, value):
        widgets = self.ui
        thickness = float(widgets.leThicknessReadOnly.text())
        newLowerLimit = thickness - value
        widgets.leLowerLimitReadOnly.setText(str(newLowerLimit.__round__(4)))

    def OnMicroSelected(self, checked):
        widgets = self.ui
        thickness = float(widgets.leThicknessReadOnly.text())
        upperTol = widgets.sbUpperTolerance.value()
        lowerTol = widgets.spLowerTolerance.value()
        if checked:
            widgets.leThicknessValue.setText(str(thickness * 1000))
            widgets.sbUpperTolerance.setValue(upperTol * 1000)
            widgets.spLowerTolerance.setValue(lowerTol * 1000)       
        else:
            widgets.leThicknessValue.setText(str(thickness / 1000))
            widgets.sbUpperTolerance.setValue(upperTol / 1000)
            widgets.spLowerTolerance.setValue(lowerTol / 1000)

        
            
        
    


        

