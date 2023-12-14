from __future__ import annotations
from concurrent.futures import thread
from email import message
from itertools import filterfalse
from math import isnan, nan
from operator import index
from statistics import covariance, mean, median, pvariance
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Windows.mainWindow import MainWindow
    
from modules.gui_modules import *
from modules.pyside_packages import *
from utils.background_worker import *
from widgets import *
from widgets.plotly_custom.plotlyWidget import PlotlyGraph
from widgets.draggableImage import DraggableImageForImageContainer
from configurations import config_global
import numpy as np
from guppy import hpy
from memory_profiler import profile

plotly_app = None

def Converter2(input: str) -> float:
    input = input.replace(',', '.')
    if input == '***' or input == 'NaN' or float(input) == 0:
        return nan
    else:
        x_float = float(input).__round__(4)
        return x_float if x_float < 2 else x_float/1000 

def Converter(x: str) -> float:
    return float(x.replace(',', '.'))

conv = {
    0: Converter,
    1: Converter,
    2: Converter2
}

def PreprocessData(filePath: str, selectedMode: str, progress_callback: SignalInstance) -> tuple:
    progress_callback.emit(0, "Loading file...")
    fileName = filePath.split('/')[-1][:-4]
    components = fileName.split('_')

    if filePath.__contains__('.txt'): 
        deliChar = '\t'
    else: 
        deliChar = ','
    array_txt = np.loadtxt(filePath, delimiter=deliChar, usecols=(0,1,2), converters=conv, encoding='utf8')

    total_step_x = int(components[1].split('x')[0])
    total_step_z = int(components[1].split('x')[1])
    step_size_x  = float(int(components[2].split('x')[0]) / total_step_x).__round__(3) 
    step_size_z  = float(int(components[2].split('x')[1]) / total_step_z).__round__(3) 

    print("Step x: ", step_size_x)
    print("Step z: ", step_size_z)

    progress_callback.emit(100, "Preprocessing data rows...")
    try:
        for row in range(total_step_z):       
            for column in range(total_step_x):
                dataLineIndex = row * total_step_x + column
                if dataLineIndex > len(array_txt) - 1: continue
                modify_z = row * step_size_z       
                array_txt[dataLineIndex][1] = round(array_txt[0][1] + modify_z, 4)

                modify_x = column * step_size_x
                array_txt[dataLineIndex][0] = round(array_txt[0][0] + modify_x, 4)

                if selectedMode == "1D" and row % 2 == 0 and column < total_step_x / 2:
                    tempVal = float(array_txt[dataLineIndex][2]) 
                    array_txt[dataLineIndex][2] = float(array_txt[row * total_step_x + total_step_x - column - 1][2]) 
                    array_txt[row * total_step_x + total_step_x - column - 1][2] = tempVal
            
            percentage = (dataLineIndex * 100) / len(array_txt)
            if int(percentage) % 20 == 0:
                progress_callback.emit(percentage, "Preprocessing data rows...")

    except IndexError:
        pass

    progress_callback.emit(100, "Done")
    return (array_txt, ComputeStatistic(array_txt))

def ComputeStatistic(data) -> dict:
    x_list = data[:, 0]
    y_list = data[:, 2]
    z_list = data[:, 1]
    y_nanRemoved = list(filterfalse(isnan, y_list))
    values, counts = np.unique(y_nanRemoved, return_counts=True)
    ind = np.argmax(counts)
    dataStatistics = dict(x_min = min(x_list),
                        y_min = min(y_nanRemoved),
                        z_min = min(z_list),
                        x_max = max(x_list),
                        y_max = max(y_nanRemoved),
                        z_max = max(z_list),
                        y_avg = mean(y_nanRemoved),
                        y_mode = values[ind],
                        y_median = median(y_nanRemoved),
                        y_variance = pvariance([value*1000 for value in y_nanRemoved]),
                        size = len(y_list))
    return dataStatistics

# WITH ACCESS TO MAIN WINDOW WIDGETS
# ///////////////////////////////////////////////////////////////
class AppFunctions():
    threadpool = QThreadPool()
    surfaceGraphs = {}
    heatmaps = {}
    plotDatas = {}
    layer1 = []
    layer2 = []
    layer3 = []
    layer4 = []
    noneLayer = []
    layers = [noneLayer, layer1, layer2, layer3, layer4]

    def setThemeHack(mainWindow: MainWindow):
        Settings.BTN_LEFT_BOX_COLOR = "background-color: #495474;"
        Settings.BTN_RIGHT_BOX_COLOR = "background-color: #495474;"
        Settings.MENU_SELECTED_STYLESHEET = MENU_SELECTED_STYLESHEET = """
        border-left: 22px solid qlineargradient(spread:pad, x1:0.034, y1:0, x2:0.216, y2:0, stop:0.499 rgba(255, 121, 198, 255), stop:0.5 rgba(85, 170, 255, 0));
        background-color: #566388;
        """

        # SET MANUAL STYLES
        #mainWindow.ui.lineEdit.setStyleSheet("background-color: #6272a4;")
        #mainWindow.ui.pushButton.setStyleSheet("background-color: #6272a4;")
        #mainWindow.ui.plainTextEdit.setStyleSheet("background-color: #6272a4;")
        mainWindow.ui.tableWidget.setStyleSheet(
            "QScrollBar:vertical { background: #6272a4; } QScrollBar:horizontal { background: #6272a4; }")
        #mainWindow.ui.scrollArea.setStyleSheet("QScrollBar:vertical { background: #6272a4; } QScrollBar:horizontal { background: #6272a4; }")
        #mainWindow.ui.comboBox.setStyleSheet("background-color: #6272a4;")
        #mainWindow.ui.horizontalScrollBar.setStyleSheet("background-color: #6272a4;")
        #mainWindow.ui.verticalScrollBar.setStyleSheet("background-color: #6272a4;")
        #mainWindow.ui.commandLinkButton.setStyleSheet("color: #ff79c6;")

    def SetDefaultProperties(mainWindow: MainWindow):
        config_global.getConfiguration()
        mainWindow.ui.leVariance.setText(str(config_global.config['Variance']))
        mainWindow.ui.cbFillHole.setChecked(config_global.config['FillHole'])

        #Added data table
        table = mainWindow.ui.tableWidget
        table.setColumnCount(3)
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Custom)
        table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Custom)
        table.horizontalHeader().setDefaultSectionSize(200)
        table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        table.setHorizontalHeaderLabels(["File names", "Layer index", "Scanned mode"])

        graphToolBox = mainWindow.ui.extraLeftBox
        graphToolBox.setMinimumWidth(0)

        #Generated graph table
        graphTable = mainWindow.ui.graphTable   
        graphTable.setColumnCount(1)
        graphTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        graphTable.verticalHeader().resizeSection(0, 100)
        font = QFont()  # Create a QFont object
        font.setPointSize(14)  # Set the font size
        graphTable.verticalHeader().setFont(font)
        graphTable.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        graphTable.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        graphTable.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        graphTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        graphTable.setSelectionMode(QAbstractItemView.SingleSelection)
        graphTable.setHorizontalHeaderLabels(["Generated Graphs"])  
        graphTable.setStyleSheet(
            """
            QTableView
            {
                color: #17111f;
                border: 2px solid #7656a6;
                background: #17111f;
                gridline-color: #d1c3e6;
            }
            QTableView::item:selected
            {
                background: #6b2782;
            }
            """
        )

        btnViewDetail = QPushButton("View Detail")
        btnDeleteGraph = QPushButton("Delete")
        btnLayout = QHBoxLayout(mainWindow.ui.graph_collection)

        btnLayout.addWidget(btnViewDetail)
        btnLayout.addWidget(btnDeleteGraph)
        mainWindow.ui.gridLayout_2.addLayout(btnLayout, 1, 0)
        mainWindow.ui.gridLayout_2.setAlignment(btnLayout, Qt.AlignBottom | Qt.AlignRight)

        btnViewDetail.setStyleSheet(
            """
            QPushButton{
                background-color: #4CAF50; 
                border-radius: 8px;
                border: none; 
                color: white;
                padding: 15px 32px; 
                text-align: center; 
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
            }

            QPushButton:hover{
                background-color: #a3e3b4;
                color: black;
            }           
            """
        )
        btnDeleteGraph.setStyleSheet(
            """
            QPushButton{
                background-color: #e01d16; 
                border-radius: 8px;
                border: none; 
                color: white;
                padding: 15px 32px; 
                text-align: center; 
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
            }

            QPushButton:hover{
                background-color: #e68d8a;
                color: black;
            }           
            """
        )
        btnViewDetail.clicked.connect(lambda: AppFunctions.ViewDetail(graphTable))
        btnDeleteGraph.clicked.connect(lambda: AppFunctions.RemoveGraphFromTable(graphTable))

        # Set progressbar
        progressBar = mainWindow.ui.progressBar
        progressLabel = mainWindow.ui.progressLabel
        progressLabel.setText('')
        progressBar.setVisible(False) 

        # Set PDF editor GraphicsView
        graphicsView = mainWindow.ui.graphicsView
        graphicsScene = graphicsView.scene()
        graphicsView.setFixedWidth(800)
        graphicsView.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        graphicsView.verticalScrollBar().setSliderPosition(0)
        graphicsView.horizontalScrollBar().setSliderPosition(0)
        graphicsGlobal.operationMode = graphicsGlobal.OperationMode.Normal
        dropRemove = XMarkItem(graphicsView.width()/2 - 20, graphicsView.height() - 100, 50)
        graphicsScene.addItem(dropRemove)
        dropRemove.hide()

        # Set image container graphic view
        imageContainer = mainWindow.ui.graphImagesContainer
        imageContainer.setScene(QGraphicsScene())
        imageContainer.setSceneRect(QRect(0, 0, 200, 800))
        imageContainer.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
       
    def updateProgressBar(progressBar:QProgressBar, progressLabel:QLabel, text, value):
        progressBar.setVisible(True)
        progressLabel.setText(text)
        progressBar.setValue(value)
    
    def resetProgressBar(progressBar:QProgressBar, progressLabel:QLabel):
        progressBar.setVisible(False)
        progressLabel.setText('')
        progressBar.setValue(0)

    def GetFileName(mainWindow: MainWindow):
        file_filter = 'Text File (*.txt); Data File (*.xlsx *.csv *.dat);; Excel File (*.xlsx *.xls);; Text File (*.txt)'
        response = QFileDialog.getOpenFileName(
            parent = mainWindow,
            caption = 'Select a file',
            #directory = os.getcwd(),
            filter = file_filter,       
            #initialFilter='Excel File (*.xlsx *.xls)'
        )
        absolutePath = str(response[0])
        fileName = absolutePath.split('/')[-1].rstrip(".txt")
        if fileName == '': 
            return None
        elif fileName in AppFunctions.plotDatas.keys():
            QMessageBox.information(mainWindow, 
                                    "Import data",
                                    f"{fileName} is aleady imported.",
                                    QMessageBox.StandardButton.Ok)
            return None
        
        #SELECT SCAN MODE (1D or FSS)
        messageBox = QMessageBox()
        messageBox.setWindowTitle("Required")
        messageBox.setText("Select scanned mode!")

        fssModeButton = messageBox.addButton("FSS Scanner", QMessageBox.ButtonRole.AcceptRole)
        oneDScannerButton = messageBox.addButton("1D Scanner", QMessageBox.ButtonRole.AcceptRole)
        messageBox.setStandardButtons(QMessageBox.StandardButton.Cancel)
        messageBox.exec()

        if messageBox.clickedButton() == fssModeButton: 
            selectedMode = "FSS"
        elif messageBox.clickedButton() == oneDScannerButton:
            selectedMode = "1D"
        else: return None
        #============================================

        print("Absolute path: ", absolutePath)
        print("File name: ", fileName)

        if str(absolutePath) != '':
            worker = Worker(PreprocessData, absolutePath, selectedMode)
            worker.signals.result.connect(
                lambda layerData:( AppFunctions.OnDataPreprocessed(mainWindow, fileName, layerData, selectedMode)))
            worker.signals.progress.connect(
                lambda percentage, text:
                    AppFunctions.updateProgressBar(mainWindow.ui.progressBar,
                                                   mainWindow.ui.progressLabel,
                                                   text, percentage))
            worker.signals.error.connect(
                lambda errTuple: (
                    QMessageBox.information(mainWindow, "Data Preprocessing",
f"""
Load data failed
- Error type: {errTuple[0]}.
- Error message: {errTuple[1]}
- Traceback: 
{errTuple[2]}
""",
                                    QMessageBox.StandardButton.Ok),
                    AppFunctions.resetProgressBar(mainWindow.ui.progressBar,
                                                   mainWindow.ui.progressLabel)),
                )
            AppFunctions.threadpool.start(worker)
            return fileName
        
        return None

    def OnDataPreprocessed(mainWindow, fileName, layerData, selectedMode):
        AppFunctions.plotDatas[fileName] = layerData
        AppFunctions.noneLayer.append(fileName)
        AppFunctions.AddFilenameRowToTable(mainWindow, fileName, selectedMode)
        AppFunctions.resetProgressBar(mainWindow.ui.progressBar,
                                    mainWindow.ui.progressLabel)

    def AddFilenameRowToTable(mainWindow, fileName, selectedMode):
        try:
            table = mainWindow.ui.tableWidget
            rowPosition = table.rowCount()
            layers = QComboBox()
            layers.addItems(['None', 'Layer 1', 'Layer 2', 'Layer 3', 'Layer 4'])
            layers.currentTextChanged.connect(lambda newText: AppFunctions.OnLayerIndexChanged(newText, table, layers))
            table.insertRow(rowPosition)
            table.setItem(rowPosition, 0, QTableWidgetItem(fileName))
            table.setCellWidget(rowPosition, 1, layers)
            table.setItem(rowPosition, 2, QTableWidgetItem(selectedMode))
        except BaseException as error:
            QMessageBox.information(None, 
                                    "Add file name to table error",
                                    f"An exception occurred: {format(error)}'.",
                                    QMessageBox.StandardButton.Ok)
 
    def OnLayerIndexChanged(layer, table:QTableWidget, comboBox:QComboBox):
        currentRow = table.indexAt(comboBox.pos()).row()
        item = table.item(currentRow, 0).text()
        match layer:
            case 'None':
                selectedLayer = AppFunctions.noneLayer
            case 'Layer 1':
                selectedLayer = AppFunctions.layer1
            case 'Layer 2':
                selectedLayer = AppFunctions.layer2
            case 'Layer 3':
                selectedLayer = AppFunctions.layer3
            case 'Layer 4':
                selectedLayer = AppFunctions.layer4

        if item not in selectedLayer:
            selectedLayer.append(item)
        AppFunctions.RemoveItemFromOtherLayer(item, selectedLayer)

        for layer in AppFunctions.layers:
            print(str(layer))

    def RemoveItemFromOtherLayer(item, selectedLayer):
        for layer in AppFunctions.layers:
            if layer is not selectedLayer and item in layer:
                layer.remove(item)

    def RemoveDataFile(dataTable: QTableWidget):
        try:
            selectedRow = dataTable.currentRow()
            item = dataTable.item(selectedRow, 0)
            dataToBeDel = AppFunctions.plotDatas[item.text()]
            np.delete(dataToBeDel, len(dataToBeDel))
            for layer in AppFunctions.layers:
                if item.text() in layer:
                    layer.remove(item.text())
            print(AppFunctions.layers)

            del AppFunctions.plotDatas[item.text()]
            dataTable.removeRow(selectedRow)
        except BaseException as error:
            QMessageBox.information(None, 
                                    "Data remove error",
                                    f"An exception occurred: {format(error)}'.",
                                    QMessageBox.StandardButton.Ok)

    def SurfaceGraphFactory(graphName: str, dataFrames, layerParams, graphImageContainer: QGraphicsView) -> SurfaceGraph:
        #Reset data in previous graph to maintain memory 
        for key in AppFunctions.surfaceGraphs.keys():
            graph = AppFunctions.surfaceGraphs.get(key)
            if graph != None:
                graph.ResetData()

        name = graphName
        if AppFunctions.surfaceGraphs.get(name) != None:
            name = graphName + "_" + str(len(AppFunctions.surfaceGraphs))

        surfaceGraph = SurfaceGraph(name, dataFrames, layerParams)
        surfaceGraph.graphImagesChanged.connect(lambda x: AppFunctions.onSurfaceGraphImagesChanged(x, surfaceGraph, graphImageContainer))
        minimum_graph_size = QSize(1000 / 2, 800 / 1.75)
        print("Initializing graph....")
        surfaceGraph.initialize(minimum_graph_size, QSize(1000,800))

        AppFunctions.surfaceGraphs[name] = surfaceGraph
        return surfaceGraph
    
    def SurfaceGraphSetUp(surfaceGraph: SurfaceGraph, progress_callback: SignalInstance):
        progress_callback.emit(0, "Adding data...")
        surfaceGraph.AddData()
        progress_callback.emit(75, "Setting axis...")
        surfaceGraph.EnableGraph()
        progress_callback.emit(100, "Done")
    
    def ScatterGraphSetUp(surfaceGraph: ScatterGraph):
        print("Adding data..."),
        surfaceGraph.AddData(),

    def ScatterGraphFactory(graphName: str, dataFrames, graphImageContainer: QGraphicsView) -> ScatterGraph:
        #Reset data in previous graph to maintain memory 
        for key in AppFunctions.surfaceGraphs.keys():
            graph = AppFunctions.surfaceGraphs.get(key)
            if graph != None:
                graph.ResetData()

        name = graphName
        if AppFunctions.surfaceGraphs.get(name) != None:
            name = graphName + "_" + str(len(AppFunctions.surfaceGraphs))

        surfaceGraph = ScatterGraph(name, dataFrames)
        surfaceGraph.graphImagesChanged.connect(lambda x: AppFunctions.onSurfaceGraphImagesChanged(x, surfaceGraph, graphImageContainer))
        minimum_graph_size = QSize(1000 / 2, 800 / 1.75)
        print("Initializing graph....")
        surfaceGraph.initialize(minimum_graph_size, QSize(1000,800))

        AppFunctions.surfaceGraphs[name] = surfaceGraph
        return surfaceGraph
    
    def HeatmapFactory(graphName: str, additionalParams)-> PlotlyGraph:
        graphName = graphName + "_Heatmap"
        heatMap = PlotlyGraph(graphName, additionalParams)
        global plotly_app
        plotly_app.init_handler(AppFunctions.heatmaps, heatMap._view.page().profile())
        AppFunctions.heatmaps[PlotlyGraph.graphNameAlias[graphName]] = heatMap
        return heatMap

    def RenderSurfaceGraph(dataTuple, mainWindow: MainWindow):
        dataFileNames, layerParams = dataTuple
        dataFrames = [AppFunctions.plotDatas[dataFileName] for dataFileName in dataFileNames]
        if len(dataFrames) != 1:
            graphName = "Multi layers"
        else:
            graphName = dataFileNames[0][:-4]
        
        surfaceGraph = AppFunctions.SurfaceGraphFactory(graphName + "_SurfaceGraph", dataFrames, layerParams, mainWindow.ui.graphImagesContainer)
        worker = Worker(AppFunctions.SurfaceGraphSetUp, surfaceGraph)

        worker.signals.result.connect(lambda:(
                                    print("Rendering images..."),
                                    surfaceGraph.RenderGraphImages(),    
                                    AppFunctions.AddSurfaceGraphToTable( mainWindow.ui.graphTable, 
                                            mainWindow.ui.graphImagesContainer,
                                            surfaceGraph),
                                    AppFunctions.resetProgressBar(mainWindow.ui.progressBar,
                                                   mainWindow.ui.progressLabel)))
        worker.signals.progress.connect(
            lambda percentage, text: 
                AppFunctions.updateProgressBar(mainWindow.ui.progressBar,
                                               mainWindow.ui.progressLabel,
                                               text, percentage))
        worker.signals.error.connect(
                lambda errTuple: (
                    QMessageBox.information(mainWindow, "Render surface graph",
f"""
Rendering failed:
- Error type: {errTuple[0]}.
- Error message: {errTuple[1]}
- Traceback: 
{errTuple[2]}
""",
                                    QMessageBox.StandardButton.Ok),
                AppFunctions.resetProgressBar(mainWindow.ui.progressBar,
                                                   mainWindow.ui.progressLabel))
        )

        AppFunctions.threadpool.start(worker) 

    def RenderScatterGraph(dataFileNames, mainWindow: MainWindow):
        dataFrames = [AppFunctions.plotDatas[dataFileName] for dataFileName in dataFileNames]
        if len(dataFrames) != 1:
            graphName = "Multi layers"
        else:
            graphName = dataFileNames[0]
        
        scatterGraph = AppFunctions.ScatterGraphFactory(graphName + "_ScatterGraph", dataFrames, mainWindow.ui.graphImagesContainer)
        worker = Worker(AppFunctions.SurfaceGraphSetUp, scatterGraph)

        worker.signals.result.connect(lambda:(
                                    # print("Rendering images..."),
                                    # scatterGraph.RenderGraphImages(),    
                                    AppFunctions.AddSurfaceGraphToTable( mainWindow.ui.graphTable, 
                                            mainWindow.ui.graphImagesContainer,
                                            scatterGraph)))
        AppFunctions.threadpool.start(worker)
        
    def PlotHeatmapPlotly(dataFileName, additionalParams, mainWindow: MainWindow):
        if dataFileName + "_Heatmap" in PlotlyGraph.graphNameAlias.keys():
            QMessageBox.information(mainWindow, 
                                    "Heatmap Renderer",
                                    f"{dataFileName} Heatmap is aleady rendered.",
                                    QMessageBox.StandardButton.Ok)
            return
        plotData, _ = AppFunctions.plotDatas[dataFileName] 
        heatMap:PlotlyGraph = AppFunctions.HeatmapFactory(dataFileName, additionalParams)
        worker = Worker(heatMap.RenderToImage, plotData)
        #heatMap.RenderToImage(plotData)
        worker.signals.result.connect(lambda :(
            heatMap.LoadUrl(),
            AppFunctions.AddHeatmapToTable(mainWindow.ui.graphTable,
                                       mainWindow.ui.graphImagesContainer,
                                       heatMap.GetGraphImage(),
                                       heatMap.graphName),
            AppFunctions.resetProgressBar(mainWindow.ui.progressBar,
                                                   mainWindow.ui.progressLabel)))                   
                                       
        worker.signals.progress.connect(
            lambda percentage, text: 
                AppFunctions.updateProgressBar(mainWindow.ui.progressBar,
                                               mainWindow.ui.progressLabel,
                                               text, percentage))
        worker.signals.error.connect(
                lambda: AppFunctions.resetProgressBar(mainWindow.ui.progressBar,
                                                   mainWindow.ui.progressLabel))
        AppFunctions.threadpool.start(worker)
    
    def AddSurfaceGraphToTable(table: QTableWidget, container: QGraphicsView, graph: SurfaceGraph):
        try:
            row_position = table.rowCount()
            table.insertRow(row_position)
            imageSurface = graph.GetSurfaceGraphImage()
            image2DSlice = graph.GetMatplotlibGraphImage()
            graphName = graph._graphName

            graphLabel = QLabel(graphName)
            cell_widget = QWidget()
            cell_layout = QGridLayout()

            cell_layout.addWidget(imageSurface, 0, 1)
            cell_layout.addWidget(image2DSlice, 0, 2)
            cell_layout.addWidget(graphLabel, 0, 3)
            cell_layout.setContentsMargins(30, 2, 2, 0)
            cell_widget.setLayout(cell_layout)

            table.setCellWidget(row_position, 0, cell_widget)
            table.setRowHeight(row_position, 350)
            
            # ADD IMAGES INTO GTAPH IMAGES CONTAINER
            index = len(container.scene().items())
            surfaceImageItem = DraggableImageForImageContainer(index, 
                                                            imageSurface, 
                                                            graphName + "-3D", 
                                                            lambda y: AppFunctions.onImageContainerItemRemoved(container, y))
            slicedImageItem = DraggableImageForImageContainer(index + 1, 
                                                            image2DSlice, 
                                                            graphName + "-2D sliced", 
                                                            lambda y: AppFunctions.onImageContainerItemRemoved(container, y))
            container.scene().addItem(surfaceImageItem)
            container.scene().addItem(slicedImageItem)
            container.setSceneRect(0, 0, container.sceneRect().width(), container.sceneRect().height() + 200)
        except BaseException as error:
            QMessageBox.information(None, 
                                    "Add graph to table error",
                                    f"An exception occurred: {format(error)}'.",
                                    QMessageBox.StandardButton.Ok)

    def AddHeatmapToTable(table: QTableWidget, container: QGraphicsView, imageHeatmap, graphName):
        try:
            # CONSTRUCT ROW AND ADD TO TABLE
            row_position = table.rowCount()
            table.insertRow(row_position)

            graphLabel = QLabel(graphName)
            cell_widget = QWidget()
            cell_layout = QGridLayout()

            cell_layout.addWidget(imageHeatmap, 0, 1)
            cell_layout.addWidget(graphLabel, 0, 3)

            cell_layout.setContentsMargins(30, 2, 2, 0)
            cell_widget.setLayout(cell_layout)

            table.setCellWidget(row_position, 0, cell_widget)
            table.setRowHeight(row_position, 350)

            index = len(container.scene().items())
            heatmapImageItem = DraggableImageForImageContainer(index, imageHeatmap, graphName)
            container.scene().addItem(heatmapImageItem)
            container.setSceneRect(0, 0, container.sceneRect().width(), container.sceneRect().height() + 200)
        except BaseException as error:
            QMessageBox.information(None, 
                                    "Add graph to table error",
                                    f"An exception occurred: {format(error)}'.",
                                    QMessageBox.StandardButton.Ok)

    def ViewDetail(table: QTableWidget):
        selectedRow = table.currentRow()
        widgets = table.cellWidget(selectedRow, 0).children()
        graphName = widgets[-1].text()
        if len(widgets) == 4:
            AppFunctions.surfaceGraphs[graphName].ViewDetail()
        else:
            #print(AppFunctions.heatmaps)
            AppFunctions.heatmaps[PlotlyGraph.graphNameAlias[graphName]].ViewDetail()

    def RemoveGraphFromTable(table: QTableWidget):
        selectedRow = table.currentRow()
        widgets = table.cellWidget(selectedRow, 0).children()
        graphName = widgets[-1].text()
        if len(widgets) == 4:
            AppFunctions.surfaceGraphs[graphName].RemoveDataSeries()
            graph: SurfaceGraph = AppFunctions.surfaceGraphs[graphName]
            graph.deleteLater()
            AppFunctions.surfaceGraphs[graphName] = None
            del AppFunctions.surfaceGraphs[graphName]
            
        else: 
            AppFunctions.heatmaps[PlotlyGraph.graphNameAlias[graphName]].deleteLater()
            del AppFunctions.heatmaps[PlotlyGraph.graphNameAlias[graphName]]
            del PlotlyGraph.graphNameAlias[graphName]
        table.removeRow(selectedRow)     
        # print(AppFunctions.surfaceGraphs)
        # print("Graph ref count:", sys.getrefcount(graph))
        # print("Graph gc ref count:", len(gc.get_referrers(graph)))
        # for reference in gc.get_referrers(graph):
        #     print(reference)
        #     print(id(graph))
        #     print("============================================")
        # print("Size of graph: ", asizeof.asizeof(graph) )

        # print("Graphs: ",len(AppFunctions.surfaceGraphs))
        # print("datas: ",len(AppFunctions.plotDatas))

        # h = hpy()
        # print(h.heap())

    def onSurfaceGraphImagesChanged(graphName: str, surfaceGraph:SurfaceGraph, container: QGraphicsView):
        print(graphName)
        graphImages = [image for image in container.scene().items() if image.imageName.find(graphName) != -1][-2:]
        for image in graphImages:
            if image.imageName.find("3D") != -1:
                label = surfaceGraph.GetSurfaceGraphImage()
            else: 
                label = surfaceGraph.GetMatplotlibGraphImage()
            
            image.setPixmap(label.pixmap().scaled(QSize(190, 120), 
                                         Qt.AspectRatioMode.IgnoreAspectRatio, 
                                         Qt.TransformationMode.SmoothTransformation))

    def onImageContainerItemRemoved(container: QGraphicsView, removedPosY):
        for image in container.scene().items():
            if image.scenePos().y() > removedPosY:
                image.setPos(image.scenePos().x(), image.scenePos().y() - image.sceneBoundingRect().height() - image.margin)
               
    def ResetImageContainer(container: QGraphicsView):
        for item in container.scene().items():
            container.scene().removeItem(item)

    def EnableParamsModify(mainWindow: MainWindow, enable):
        buttonSave = mainWindow.ui.btnSaveParams
        varianceField = mainWindow.ui.leVariance
        cbFillHole = mainWindow.ui.cbFillHole
        if enable:
            buttonSave.setText("Save")
            buttonSave.setIcon(QIcon(":/icons/images/icons/cil-save.png"))
            varianceField.setReadOnly(False)
            cbFillHole.setCheckable(True)
        else:
            buttonSave.setText("Modify")
            buttonSave.setIcon(QIcon(":/icons/images/icons/cil-pencil.png"))
            varianceField.setReadOnly(True)
            cbFillHole.setCheckable(False)
    
    def SaveParameters(mainWindow: MainWindow):
        config_global.isModifying = not config_global.isModifying
        if config_global.isModifying:
            AppFunctions.EnableParamsModify(mainWindow, True)
        else:
            AppFunctions.EnableParamsModify(mainWindow, False)
            config_global.updateNewConfiguration(varianceValue=float(mainWindow.ui.leVariance.text()),
                                                 fillHoleValue=mainWindow.ui.cbFillHole.isChecked())