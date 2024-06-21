import os
import sys
from turtle import width

from pandas import wide_to_long
# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from modules import *
from widgets import *

os.environ["QT_FONT_DPI"] = "96" # FIX Problem for High DPI and Scale above 100%

# SET AS GLOBAL WIDGETS
# ///////////////////////////////////////////////////////////////
widgets = None

class MainWindow(QMainWindow):
    def __init__(self, app: QApplication):
        super().__init__()
        
        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.app = app
        self.scatter = None
        global widgets
        widgets = self.ui

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = "GES HeatMap App"
        description = "GES Data Visualizer"
        widgets.version.setText(Settings.VERSION)
        # APPLY TEXTS
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        # TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)

        # QTableWidget PARAMETERS
        # ///////////////////////////////////////////////////////////////
        widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////

        # LEFT MENUS
        widgets.btn_home.clicked.connect(self.ButtonCliked)
        widgets.btn_AddData.clicked.connect(self.ButtonCliked)
        widgets.btn_AddFile.clicked.connect(widgets.btn_AddData.click)
        widgets.btn_export.clicked.connect(self.ButtonCliked)
        widgets.btn_PDFeditor.clicked.connect(widgets.btn_export.click)
        widgets.btnGraphCollection.clicked.connect(self.ButtonCliked)
        widgets.btn_open.clicked.connect(self.ButtonCliked)
        widgets.btn_removeData.clicked.connect(self.ButtonCliked)

        # EXTRA LEFT BOX
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)
            
        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # EXTRA RIGHT BOX
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)
        widgets.settingsTopBtn.clicked.connect(openCloseRightBox)

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()
        widgets.toggleButton.click()

        # SET CUSTOM THEME
        # ///////////////////////////////////////////////////////////////
        useCustomTheme = False
        themeFile = "themes\py_dracula_light.qss"

        # SET THEME AND HACKS
        if useCustomTheme:
            # LOAD AND APPLY STYLE
            UIFunctions.theme(self, themeFile, True)

            # SET HACKS
            AppFunctions.setThemeHack(self)

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))
        # widgets.btn_lineGraph.clicked.connect(self.PlotButtonClicked)
        widgets.btn_pointCloud.clicked.connect(self.PlotButtonClicked)
        widgets.btn_heatMap.clicked.connect(self.PlotButtonClicked)
        widgets.btn_PlotSurface.clicked.connect(widgets.btn_pointCloud.click)
        widgets.btn_PlotHeatmap.clicked.connect(widgets.btn_heatMap.click)

        # PDF EDITOR MENU
        widgets.btnPan.clicked.connect(self.PdfEditorModeChanged)
        widgets.btnRemoveItem.clicked.connect(self.PdfEditorModeChanged)
        widgets.btnSelect.clicked.connect(self.PdfEditorModeChanged)

        # PDF TOOL BUTTONS
        widgets.btnAddText.clicked.connect(self.PdfToolBtnClicked)
        widgets.btnNewPage.clicked.connect(self.PdfToolBtnClicked)
        widgets.btnAddNewPage.clicked.connect(self.PdfToolBtnClicked)
        widgets.btnSavePdf.clicked.connect(self.PdfToolBtnClicked)

        widgets.btnResetContainer.clicked.connect(lambda: ImageContainerResetClockedHandler(self))
        widgets.btn_exit.clicked.connect(self.close)
        widgets.btnSaveParams.clicked.connect(lambda: ParametersSaveButtonClickedHandler(self))

        #SET DEFAULT WIDGETS PROPERTIES
        AppFunctions.SetDefaultProperties(self)

    def ButtonCliked(self):
        sender = self.sender()
        MenuButtonClickedHandler(sender, self)

    def PlotButtonClicked(self):
        sender = self.sender()
        PlottingButtonClickedHandler(sender, self)

    def PdfEditorModeChanged(self):
        sender = self.sender()
        PdfEditorModeChangedHandler(sender, self)

    def PdfToolBtnClicked(self):
        sender = self.sender()
        PdfToolBtnsClickedHandler(sender, self)

    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

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

    def closeEvent(self, event):
        button = QMessageBox.information(self, "Close Application",
                                f"Do you want to close application ?",
                                QMessageBox.StandardButton.Ok,
                                QMessageBox.StandardButton.Cancel)
        if button == QMessageBox.StandardButton.Ok:
            folder_path = 'PlotImages'
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if file.endswith('.png') or file.endswith('.html'):
                        os.remove(os.path.join(root, file))
            event.accept()
        else: event.ignore()

def RunApp():
    app_functions.plotly_app = PlotlyApplication()
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("GESLogo.ico"))
    window = MainWindow(app)
    sys.exit(app.exec())

