from __future__ import annotations
from typing import TYPE_CHECKING
from modules.pyside_packages import *
from modules.gui_modules import *
from modules.data_manipulate import *
from widgets import *


if TYPE_CHECKING:
    from Windows.mainWindow import MainWindow

# BUTTONS CLICK
# Post here your functions for clicked buttons
# ///////////////////////////////////////////////////////////////

def ImageContainerResetClockedHandler(mainWindow: MainWindow):
    container = mainWindow.ui.graphImagesContainer
    button = QMessageBox.warning(mainWindow, "Warning",
                             "This will remove every images in this container. Continue ?",
                               QMessageBox.StandardButton.Ok,
                                 QMessageBox.StandardButton.Cancel)
        
    if button == QMessageBox.StandardButton.Ok:
        AppFunctions.ResetImageContainer(container)
        container.setSceneRect(QRect(0, 0, 200, 800))
              
def ParametersSaveButtonClickedHandler(mainWindow: MainWindow):
    AppFunctions.SaveParameters(mainWindow)

def MenuButtonClickedHandler(sender: QObject, mainWindow: MainWindow):
    # GET BUTTON CLICKED
    btn = sender
    btnName = btn.objectName()
    widgets = mainWindow.ui

    # SHOW HOME PAGE
    if btnName == "btn_home":
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        UIFunctions.resetStyle(mainWindow, btnName)
        btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

    # SHOW WIDGETS PAGE
    if btnName == "btn_AddData" :
        widgets.stackedWidget.setCurrentWidget(widgets.page_add_data)
        UIFunctions.resetStyle(mainWindow, btnName)
        btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

    # SHOW NEW PAGE
    if btnName == "btn_export":
        widgets.stackedWidget.setCurrentWidget(widgets.new_page) # SET PAGE
        UIFunctions.resetStyle(mainWindow, btnName) # RESET ANOTHERS BUTTONS SELECTED
        btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU

    if btnName == "btnGraphCollection":
        widgets.stackedWidget.setCurrentWidget(widgets.graph_collection) # SET PAGE
        UIFunctions.resetStyle(mainWindow, btnName) # RESET ANOTHERS BUTTONS SELECTED
        btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU

    if btnName == "btn_save":
        print("Save BTN clicked!")

    if btnName == "btn_open":
        AppFunctions.GetFileName(mainWindow)

    if btnName == "btn_removeData":
        AppFunctions.RemoveDataFile(widgets.tableWidget)

    # PRINT BTN NAME
    print(f'Button "{btnName}" pressed!')

def PlottingButtonClickedHandler(sender: QObject, mainWindow: MainWindow):
    btn = sender
    btnName = btn.objectName()
    widgets = mainWindow.ui

    if btnName == "btn_lineGraph":
        PlotLineGraphMatplotlib(widgets.line_graph_placeholder)

    if btnName == "btn_pointCloud":
        layerSelectWindow = LayerSelectionWindow(AppFunctions.layers, AppFunctions.plotDatas)
        layerSelectWindow.dataSubmitted.connect(lambda submittedData: PlotSurfaceGraphQt(mainWindow, submittedData))
        layerSelectWindow.show()
        
    if btnName == "btn_heatMap":
        layerSelectWindow = LayerSelectionWindow(AppFunctions.layers, AppFunctions.plotDatas)
        layerSelectWindow.dataSubmitted.connect(lambda submittedData: PlotHeatMapQt(mainWindow, submittedData))
        layerSelectWindow.show()
    
def PdfEditorModeChangedHandler(sender: QObject, mainWindow: MainWindow):
    btn:QPushButton = sender
    btnName = btn.objectName()
    widgets = mainWindow.ui
    if btnName == "btnSelect":
        btn.setStyleSheet("background: #d9bceb;")
        icon = QIcon()
        icon.addFile(u":/icons/images/icons/mouse-pointer_focus.png", QSize(), QIcon.Normal, QIcon.Off)
        btn.setIcon(icon)
        btn.setIconSize(QSize(25, 25))

        widgets.btnPan.setStyleSheet("")
        icon = QIcon()
        icon.addFile(u":/icons/images/icons/move_disabled.png", QSize(), QIcon.Normal, QIcon.Off)
        widgets.btnPan.setIcon(icon)
        widgets.btnPan.setIconSize(QSize(25, 25))

        widgets.btnRemoveItem.setStyleSheet("")
        icon = QIcon()
        icon.addFile(u":/icons/images/icons/x_disabled.png", QSize(), QIcon.Normal, QIcon.Off)
        widgets.btnRemoveItem.setIcon(icon)
        widgets.btnRemoveItem.setIconSize(QSize(25, 25))

        graphicsGlobal.operationMode = graphicsGlobal.OperationMode.Normal
        widgets.graphicsView.update()
    elif btnName == "btnPan":
        btn.setStyleSheet("background: #d9bceb;")
        icon = QIcon()
        icon.addFile(u":/icons/images/icons/move_focus.png", QSize(), QIcon.Normal, QIcon.Off)
        btn.setIcon(icon)
        btn.setIconSize(QSize(25, 25))

        widgets.btnSelect.setStyleSheet("")
        icon = QIcon()
        icon.addFile(u":/icons/images/icons/mouse-pointer_disabled.png", QSize(), QIcon.Normal, QIcon.Off)
        widgets.btnSelect.setIcon(icon)
        widgets.btnSelect.setIconSize(QSize(25, 25))

        widgets.btnRemoveItem.setStyleSheet("")
        icon = QIcon()
        icon.addFile(u":/icons/images/icons/x_disabled.png", QSize(), QIcon.Normal, QIcon.Off)
        widgets.btnRemoveItem.setIcon(icon)
        widgets.btnRemoveItem.setIconSize(QSize(25, 25))

        graphicsGlobal.operationMode = graphicsGlobal.OperationMode.Pan
        widgets.graphicsView.update()
    elif btnName == "btnRemoveItem":
        btn.setStyleSheet("background: #d9bceb;")
        icon = QIcon()
        icon.addFile(u":/icons/images/icons/x_focus.png", QSize(), QIcon.Normal, QIcon.Off)
        btn.setIcon(icon)
        btn.setIconSize(QSize(25, 25))

        widgets.btnSelect.setStyleSheet("")
        icon = QIcon()
        icon.addFile(u":/icons/images/icons/mouse-pointer_disabled.png", QSize(), QIcon.Normal, QIcon.Off)
        widgets.btnSelect.setIcon(icon)
        widgets.btnSelect.setIconSize(QSize(25, 25))

        widgets.btnPan.setStyleSheet("")
        icon = QIcon()
        icon.addFile(u":/icons/images/icons/move_disabled.png", QSize(), QIcon.Normal, QIcon.Off)
        widgets.btnPan.setIcon(icon)
        widgets.btnPan.setIconSize(QSize(25, 25))

        graphicsGlobal.operationMode = graphicsGlobal.OperationMode.Remove
        widgets.graphicsView.update()
        
def PdfToolBtnsClickedHandler(sender: QObject, mainWindow: MainWindow):
    btn = sender
    btnName = btn.objectName()
    widgets = mainWindow.ui

    if btnName == "btnAddText":
        mainWindow.ui.graphicsView.prepareToAddtextItem()

        #widgets.graphicsView.insertTextItem()
    elif btnName == "btnNewPage":
        button = QMessageBox.warning(mainWindow, "New page warning",
                             "This will remove every elements in the canvas. Continue ?",
                               QMessageBox.StandardButton.Ok,
                                 QMessageBox.StandardButton.Cancel)
        
        if button == QMessageBox.StandardButton.Ok:
           widgets.graphicsView.resetScene()    
    elif btnName == "btnAddNewPage":
        widgets.graphicsView.addNewPage()
    elif btnName == "btnSavePdf":
        widgets.graphicsView.printToPdf()