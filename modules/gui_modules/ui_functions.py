from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Windows.mainWindow import MainWindow

from modules.pyside_packages import *
from modules.gui_modules import *
from widgets import *

# GLOBALS
# ///////////////////////////////////////////////////////////////
GLOBAL_STATE = False
GLOBAL_TITLE_BAR = True

class UIFunctions():
    # MAXIMIZE/RESTORE
    # ///////////////////////////////////////////////////////////////
    @staticmethod
    def maximize_restore(mainWindow: MainWindow):
        global GLOBAL_STATE
        status = GLOBAL_STATE
        if status == False:
            mainWindow.showMaximized()
            GLOBAL_STATE = True
            mainWindow.ui.maximizeRestoreAppBtn.setToolTip("Restore")
            mainWindow.ui.maximizeRestoreAppBtn.setIcon(QIcon(u":/icons/images/icons/icon_restore.png"))
            mainWindow.ui.frame_size_grip.hide()
            mainWindow.left_grip.hide()
            mainWindow.right_grip.hide()
            mainWindow.top_grip.hide()
            mainWindow.bottom_grip.hide()
            print(mainWindow.ui.graphImagesContainer.size().height())
        else:
            GLOBAL_STATE = False
            mainWindow.showNormal()
            mainWindow.resize(mainWindow.width()+1, mainWindow.height()+1)
            mainWindow.ui.maximizeRestoreAppBtn.setToolTip("Maximize")
            mainWindow.ui.maximizeRestoreAppBtn.setIcon(QIcon(u":/icons/images/icons/icon_maximize.png"))
            mainWindow.ui.frame_size_grip.show()
            mainWindow.left_grip.show()
            mainWindow.right_grip.show()
            mainWindow.top_grip.show()
            mainWindow.bottom_grip.show()

    # RETURN STATUS
    # ///////////////////////////////////////////////////////////////
    def returStatus():
        return GLOBAL_STATE

    # SET STATUS
    # ///////////////////////////////////////////////////////////////
    def setStatus(status):
        global GLOBAL_STATE
        GLOBAL_STATE = status

    # TOGGLE MENU
    # ///////////////////////////////////////////////////////////////
    def toggleMenu(mainWindow: MainWindow, enable):
        if enable:
            # GET WIDTH
            width = mainWindow.ui.leftMenuBg.width()
            maxExtend = Settings.MENU_WIDTH
            standard = 60

            # SET MAX WIDTH
            if width == 60:
                widthExtended = maxExtend
            else:
                widthExtended = standard

            # ANIMATION
            mainWindow.animation = QPropertyAnimation(mainWindow.ui.leftMenuBg, b"minimumWidth")
            mainWindow.animation.setDuration(Settings.TIME_ANIMATION)
            mainWindow.animation.setStartValue(width)
            mainWindow.animation.setEndValue(widthExtended)
            mainWindow.animation.setEasingCurve(QEasingCurve.InOutQuart)
            mainWindow.animation.start()

    # TOGGLE LEFT BOX
    # ///////////////////////////////////////////////////////////////
    def toggleLeftBox(mainWindow: MainWindow, enable):
        if enable:
            # GET WIDTH
            width = mainWindow.ui.extraLeftBox.width()
            widthRightBox = mainWindow.ui.extraRightBox.width()
            maxExtend = Settings.LEFT_BOX_WIDTH
            color = Settings.BTN_LEFT_BOX_COLOR
            standard = 0

            # GET BTN STYLE
            style = mainWindow.ui.toggleLeftBox.styleSheet()

            # SET MAX WIDTH
            if width == 0:
                widthExtended = maxExtend
                # SELECT BTN
                mainWindow.ui.toggleLeftBox.setStyleSheet(style + color)
                if widthRightBox != 0:
                    style = mainWindow.ui.settingsTopBtn.styleSheet()
                    mainWindow.ui.settingsTopBtn.setStyleSheet(style.replace(Settings.BTN_RIGHT_BOX_COLOR, ''))
            else:
                widthExtended = standard
                # RESET BTN
                mainWindow.ui.toggleLeftBox.setStyleSheet(style.replace(color, ''))
                
        UIFunctions.start_box_animation(mainWindow, width, widthRightBox, "left")

    # TOGGLE RIGHT BOX
    # ///////////////////////////////////////////////////////////////
    def toggleRightBox(mainWindow: MainWindow, enable):
        if enable:
            # GET WIDTH
            width = mainWindow.ui.extraRightBox.width()
            widthLeftBox = mainWindow.ui.extraLeftBox.width()
            maxExtend = Settings.RIGHT_BOX_WIDTH
            color = Settings.BTN_RIGHT_BOX_COLOR
            standard = 0

            # GET BTN STYLE
            style = mainWindow.ui.settingsTopBtn.styleSheet()

            # SET MAX WIDTH
            if width == 0:
                widthExtended = maxExtend
                # SELECT BTN
                mainWindow.ui.settingsTopBtn.setStyleSheet(style + color)
                if widthLeftBox != 0:
                    style = mainWindow.ui.toggleLeftBox.styleSheet()
                    mainWindow.ui.toggleLeftBox.setStyleSheet(style.replace(Settings.BTN_LEFT_BOX_COLOR, ''))
            else:
                widthExtended = standard
                # RESET BTN
                mainWindow.ui.settingsTopBtn.setStyleSheet(style.replace(color, ''))

            UIFunctions.start_box_animation(mainWindow, widthLeftBox, width, "right")

    def start_box_animation(mainWindow: MainWindow, left_box_width, right_box_width, direction):
        right_width = 0
        left_width = 0 
        
        # Check values
        if left_box_width == 0 and direction == "left":
            left_width = 240
        else:
            left_width = 0
        # Check values
        if right_box_width == 0 and direction == "right":
            right_width = 240
        else:
            right_width = 0       

        # ANIMATION LEFT BOX        
        mainWindow.left_box = QPropertyAnimation(mainWindow.ui.extraLeftBox, b"minimumWidth")
        mainWindow.left_box.setDuration(Settings.TIME_ANIMATION)
        mainWindow.left_box.setStartValue(left_box_width)
        mainWindow.left_box.setEndValue(left_width)
        mainWindow.left_box.setEasingCurve(QEasingCurve.InOutQuart)

        # ANIMATION RIGHT BOX        
        mainWindow.right_box = QPropertyAnimation(mainWindow.ui.extraRightBox, b"minimumWidth")
        mainWindow.right_box.setDuration(Settings.TIME_ANIMATION)
        mainWindow.right_box.setStartValue(right_box_width)
        mainWindow.right_box.setEndValue(right_width)
        mainWindow.right_box.setEasingCurve(QEasingCurve.InOutQuart)

        # GROUP ANIMATION
        mainWindow.group = QParallelAnimationGroup()
        mainWindow.group.addAnimation(mainWindow.left_box)
        mainWindow.group.addAnimation(mainWindow.right_box)
        mainWindow.group.start()

    # SELECT/DESELECT MENU
    # ///////////////////////////////////////////////////////////////
    # SELECT
    def selectMenu(getStyle):
        select = getStyle + Settings.MENU_SELECTED_STYLESHEET
        return select

    # DESELECT
    def deselectMenu(getStyle):
        deselect = getStyle.replace(Settings.MENU_SELECTED_STYLESHEET, "")
        return deselect

    # START SELECTION
    def selectStandardMenu(mainWindow: MainWindow, widget):
        for w in mainWindow.ui.topMenu.findChildren(QPushButton):
            if w.objectName() == widget:
                w.setStyleSheet(UIFunctions.selectMenu(w.styleSheet()))

    # RESET SELECTION
    def resetStyle(mainWindow, widget):
        for w in mainWindow.ui.topMenu.findChildren(QPushButton):
            if w.objectName() != widget:
                w.setStyleSheet(UIFunctions.deselectMenu(w.styleSheet()))
        # if widget.objectName() != mainWindow.ui.toggleLeftBox.objectName() and mainWindow.ui.extraLeftBox.width() != 0: 
        #     mainWindow.ui.extraCloseColumnBtn.clicked.emit()


    # IMPORT THEMES FILES QSS/CSS
    # ///////////////////////////////////////////////////////////////
    def theme(self, file, useCustomTheme):
        if useCustomTheme:
            str = open(file, 'r').read()
            self.ui.styleSheet.setStyleSheet(str)

    # START - GUI DEFINITIONS
    # ///////////////////////////////////////////////////////////////
    def uiDefinitions(mainWindow: MainWindow):
        mainWindow.ui.tableWidget.setSizePolicy
        def dobleClickMaximizeRestore(event):
            # IF DOUBLE CLICK CHANGE STATUS
            if event.type() == QEvent.MouseButtonDblClick:
                QTimer.singleShot(250, lambda: UIFunctions.maximize_restore(mainWindow))
        mainWindow.ui.titleRightInfo.mouseDoubleClickEvent = dobleClickMaximizeRestore

        if Settings.ENABLE_CUSTOM_TITLE_BAR:
            #STANDARD TITLE BAR
            mainWindow.setWindowFlags(Qt.FramelessWindowHint)
            mainWindow.setAttribute(Qt.WA_TranslucentBackground)

            # MOVE WINDOW / MAXIMIZE / RESTORE
            def moveWindow(event):
                # IF MAXIMIZED CHANGE TO NORMAL
                if UIFunctions.returStatus():
                    UIFunctions.maximize_restore(mainWindow)
                # MOVE WINDOW
                if event.buttons() == Qt.LeftButton:
                    delta = QPoint((event.globalPosition() - mainWindow.dragPos).x(), (event.globalPosition() - mainWindow.dragPos).y())
                    mainWindow.move(mainWindow.pos() + delta)
                    mainWindow.dragPos = event.globalPos()
                    event.accept()
            mainWindow.ui.titleRightInfo.mouseMoveEvent = moveWindow

            # CUSTOM GRIPS
            mainWindow.left_grip = CustomGrip(mainWindow, Qt.LeftEdge, True)
            mainWindow.right_grip = CustomGrip(mainWindow, Qt.RightEdge, True)
            mainWindow.top_grip = CustomGrip(mainWindow, Qt.TopEdge, True)
            mainWindow.bottom_grip = CustomGrip(mainWindow, Qt.BottomEdge, True)

        else:
            mainWindow.ui.appMargins.setContentsMargins(0, 0, 0, 0)
            mainWindow.ui.minimizeAppBtn.hide()
            mainWindow.ui.maximizeRestoreAppBtn.hide()
            mainWindow.ui.closeAppBtn.hide()
            mainWindow.ui.frame_size_grip.hide()

        # DROP SHADOW
        mainWindow.shadow = QGraphicsDropShadowEffect(mainWindow)
        mainWindow.shadow.setBlurRadius(17)
        mainWindow.shadow.setXOffset(0)
        mainWindow.shadow.setYOffset(0)
        mainWindow.shadow.setColor(QColor(0, 0, 0, 150))
        mainWindow.ui.bgApp.setGraphicsEffect(mainWindow.shadow)

        # RESIZE WINDOW
        mainWindow.sizegrip = QSizeGrip(mainWindow.ui.frame_size_grip)
        mainWindow.sizegrip.setStyleSheet("width: 20px; height: 20px; margin 0px; padding: 0px;")

        # MINIMIZE
        mainWindow.ui.minimizeAppBtn.clicked.connect(lambda: mainWindow.showMinimized())

        # MAXIMIZE/RESTORE
        mainWindow.ui.maximizeRestoreAppBtn.clicked.connect(lambda: UIFunctions.maximize_restore(mainWindow))

        # CLOSE APPLICATION
        mainWindow.ui.closeAppBtn.clicked.connect(lambda: mainWindow.close())

    def resize_grips(self):
        if Settings.ENABLE_CUSTOM_TITLE_BAR:
            self.left_grip.setGeometry(0, 10, 10, self.height())
            self.right_grip.setGeometry(self.width() - 10, 10, 10, self.height())
            self.top_grip.setGeometry(0, 0, self.width(), 10)
            self.bottom_grip.setGeometry(0, self.height() - 10, self.width(), 10)
    
        
    # ///////////////////////////////////////////////////////////////
    # END - GUI DEFINITIONS
