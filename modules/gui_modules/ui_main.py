# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGraphicsView,
    QGridLayout, QGroupBox, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QProgressBar,
    QPushButton, QSizePolicy, QSpacerItem, QStackedWidget,
    QTableWidget, QTableWidgetItem, QToolButton, QVBoxLayout,
    QWidget)

from widgets import *
from .resources_rc import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(940, 720)
        MainWindow.setMinimumSize(QSize(940, 560))
        self.styleSheet = QWidget(MainWindow)
        self.styleSheet.setObjectName(u"styleSheet")
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.styleSheet.setFont(font)
        self.styleSheet.setStyleSheet(u"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"\n"
"SET APP STYLESHEET - FULL STYLES HERE\n"
"DARK THEME - DRACULA COLOR BASED\n"
"\n"
"///////////////////////////////////////////////////////////////////////////////////////////////// */\n"
"\n"
"QWidget{\n"
"	color: rgb(221, 221, 221);\n"
"	font: 10pt \"Segoe UI\";\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Tooltip */\n"
"QToolTip {\n"
"	color: #ffffff;\n"
"	background-color: rgba(33, 37, 43, 180);\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"	background-image: none;\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 2px solid rgb(255, 121, 198);\n"
"	text-align: left;\n"
"	padding-left: 8px;\n"
"	margin: 0px;\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Bg App */\n"
"#bgApp {	\n"
"	background"
                        "-color: rgb(40, 44, 52);\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Left Menu */\n"
"#leftMenuBg {	\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"#topLogo {\n"
"	background-color: rgb(33, 37, 43);\n"
"	background-position: centered;\n"
"	background-repeat: no-repeat;\n"
"}\n"
"#titleLeftApp { font: 63 12pt \"Segoe UI Semibold\"; }\n"
"#titleLeftDescription { font: 8pt \"Segoe UI\"; color: rgb(189, 147, 249); }\n"
"\n"
"/* MENUS */\n"
"#topMenu .QPushButton {	\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color: transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#topMenu .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#topMenu .QPushButton:pressed {	\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"#bottomMen"
                        "u .QPushButton {	\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 20px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#bottomMenu .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#bottomMenu .QPushButton:pressed {	\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"#leftMenuFrame{\n"
"	border-top: 3px solid rgb(44, 49, 58);\n"
"}\n"
"\n"
"/* Toggle Button */\n"
"#toggleButton {\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 20px solid transparent;\n"
"	background-color: rgb(37, 41, 48);\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"	color: rgb(113, 126, 149);\n"
"}\n"
"#toggleButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#toggleButton:pressed {\n"
"	background-color: rgb(189, 147, 249);\n"
"}\n"
"\n"
"/* Title Menu */\n"
"#titleRightInf"
                        "o { padding-left: 10px; }\n"
"\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Extra Tab */\n"
"#extraLeftBox {	\n"
"	background-color: rgb(44, 49, 58);\n"
"}\n"
"#extraTopBg{	\n"
"	background-color: rgb(189, 147, 249)\n"
"}\n"
"\n"
"/* Icon */\n"
"#extraIcon {\n"
"	background-position: center;\n"
"	background-repeat: no-repeat;\n"
"	background-image: url(:/icons/images/icons/icon_settings.png);\n"
"}\n"
"\n"
"/* Label */\n"
"#extraLabel { color: rgb(255, 255, 255); }\n"
"\n"
"/* Btn Close */\n"
"#extraCloseColumnBtn { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\n"
"#extraCloseColumnBtn:hover { background-color: rgb(196, 161, 249); border-style: solid; border-radius: 4px; }\n"
"#extraCloseColumnBtn:pressed { background-color: rgb(180, 141, 238); border-style: solid; border-radius: 4px; }\n"
"\n"
"/* Extra Content */\n"
"#extraContent{\n"
"	border-top: 3px solid rgb(40, 44, 52);\n"
"}\n"
"\n"
"/* Extra Top Menus"
                        " */\n"
"#extraTopMenu .QPushButton  {\n"
"background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#extraTopMenu .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#extraTopMenu .QPushButton:pressed {	\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Content App */\n"
"#contentTopBg{	\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"#contentBottom{\n"
"	border-top: 3px solid rgb(44, 49, 58);\n"
"}\n"
"\n"
"/* Top Buttons */\n"
"#rightButtons .QPushButton { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\n"
"#rightButtons .QPushButton:hover { background-color: rgb(44, 49, 57); border-style: solid; border-radius: 4px; }\n"
"#rightButtons .QPushButton:p"
                        "ressed { background-color: rgb(23, 26, 30); border-style: solid; border-radius: 4px; }\n"
"\n"
"/* Theme Settings */\n"
"#extraRightBox { background-color: rgb(44, 49, 58); }\n"
"#themeSettingsTopDetail { background-color: rgb(189, 147, 249); }\n"
"\n"
"/* Bottom Bar */\n"
"#bottomBar { background-color: rgb(44, 49, 58); }\n"
"#bottomBar QLabel { font-size: 11px; color: rgb(113, 126, 149); padding-left: 10px; padding-right: 10px; padding-bottom: 2px; }\n"
"\n"
"/* CONTENT SETTINGS */\n"
"/* MENUS */\n"
"#contentSettings .QPushButton {	\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#contentSettings .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#contentSettings .QPushButton:pressed {	\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"/* //////////////////////////////"
                        "///////////////////////////////////////////////////////////////////\n"
"QTableWidget */\n"
"QTableWidget {	\n"
"	background-color: transparent;\n"
"	padding: 10px;\n"
"	border-radius: 5px;\n"
"	gridline-color: rgb(44, 49, 58);\n"
"	border-bottom: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item{\n"
"	border-color: rgb(44, 49, 60);\n"
"	padding-left: 5px;\n"
"	padding-right: 5px;\n"
"	gridline-color: rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item:selected{\n"
"	background-color: rgb(189, 147, 249);\n"
"}\n"
"QHeaderView::section{\n"
"	background-color: rgb(33, 37, 43);\n"
"	max-width: 30px;\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"	border-style: none;\n"
"    border-bottom: 1px solid rgb(44, 49, 60);\n"
"    border-right: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::horizontalHeader {	\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"QHeaderView::section:horizontal\n"
"{\n"
"    border: 1px solid rgb(33, 37, 43);\n"
"	background-color: rgb(33, 37, 43);\n"
"	padding: 3px;\n"
"	border-top-left-rad"
                        "ius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"}\n"
"QHeaderView::section:vertical\n"
"{\n"
"    border: 1px solid rgb(44, 49, 60);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"LineEdit */\n"
"QLineEdit {\n"
"	background-color: rgb(33, 37, 43);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(33, 37, 43);\n"
"	padding-left: 10px;\n"
"	selection-color: rgb(255, 255, 255);\n"
"	selection-background-color: rgb(255, 121, 198);\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"PlainTextEdit */\n"
"QPlainTextEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	padding: 10px;\n"
"	selection-color: rgb(255, 255, 255);\n"
"	selection-background-color: rgb(255, 121, 198);\n"
"}\n"
"QPlainTextEdit  QScrollBar:ve"
                        "rtical {\n"
"    width: 8px;\n"
" }\n"
"QPlainTextEdit  QScrollBar:horizontal {\n"
"    height: 8px;\n"
" }\n"
"QPlainTextEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QPlainTextEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"ScrollBars */\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 8px;\n"
"    margin: 0px 21px 0 21px;\n"
"	border-radius: 0px;\n"
"}\n"
"QScrollBar::handle:horizontal {\n"
"    background: rgb(189, 147, 249);\n"
"    min-width: 25px;\n"
"	border-radius: 4px\n"
"}\n"
"QScrollBar::add-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"	border-top-right-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"    subcontrol-position: right;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::sub-line:horizontal {\n"
"    border: none;\n"
"   "
                        " background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"	border-top-left-radius: 4px;\n"
"    border-bottom-left-radius: 4px;\n"
"    subcontrol-position: left;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
" QScrollBar:vertical {\n"
"	border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 8px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius: 0px;\n"
" }\n"
" QScrollBar::handle:vertical {	\n"
"	background: rgb(189, 147, 249);\n"
"    min-height: 25px;\n"
"	border-radius: 4px\n"
" }\n"
" QScrollBar::add-line:vertical {\n"
"     border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"	border-bottom-left-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"     subcontrol-position: bottom;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::sub-line:verti"
                        "cal {\n"
"	border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"	border-top-left-radius: 4px;\n"
"    border-top-right-radius: 4px;\n"
"     subcontrol-position: top;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
" QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"CheckBox */\n"
"QCheckBox::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QCheckBox::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    background: 3px solid rgb(52, 59, 72);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"	background-image: url(:/icons/images/icons/cil-check-alt.png);\n"
""
                        "}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"RadioButton */\n"
"QRadioButton::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QRadioButton::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    background: 3px solid rgb(94, 106, 130);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"ComboBox */\n"
"QComboBox{\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(33, 37, 43);\n"
"	padding: 5px;\n"
"	padding-left: 10px;\n"
"}\n"
"QComboBox:hover{\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QComboBox::drop-down {\n"
"	subcontrol-origin: padding;\n"
"	subcontrol-position: top right;\n"
"	width: 25px; \n"
"	border-left-"
                        "width: 3px;\n"
"	border-left-color: rgba(39, 44, 54, 150);\n"
"	border-left-style: solid;\n"
"	border-top-right-radius: 3px;\n"
"	border-bottom-right-radius: 3px;	\n"
"	background-image: url(:/icons/images/icons/cil-arrow-bottom.png);\n"
"	background-position: center;\n"
"	background-repeat: no-reperat;\n"
" }\n"
"QComboBox QAbstractItemView {\n"
"	color: rgb(255, 121, 198);	\n"
"	background-color: rgb(33, 37, 43);\n"
"	padding: 10px;\n"
"	selection-background-color: rgb(39, 44, 54);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Sliders */\n"
"QSlider::groove:horizontal {\n"
"    border-radius: 5px;\n"
"    height: 10px;\n"
"	margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:horizontal:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:horizontal {\n"
"    background-color: rgb(189, 147, 249);\n"
"    border: none;\n"
"    height: 10px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	bor"
                        "der-radius: 5px;\n"
"}\n"
"QSlider::handle:horizontal:hover {\n"
"    background-color: rgb(195, 155, 255);\n"
"}\n"
"QSlider::handle:horizontal:pressed {\n"
"    background-color: rgb(255, 121, 198);\n"
"}\n"
"\n"
"QSlider::groove:vertical {\n"
"    border-radius: 5px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:vertical:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:vertical {\n"
"    background-color: rgb(189, 147, 249);\n"
"	border: none;\n"
"    height: 10px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	border-radius: 5px;\n"
"}\n"
"QSlider::handle:vertical:hover {\n"
"    background-color: rgb(195, 155, 255);\n"
"}\n"
"QSlider::handle:vertical:pressed {\n"
"    background-color: rgb(255, 121, 198);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"CommandLinkButton */\n"
"QCommandLinkButton {	\n"
"	color: rgb(255, 121, 198);\n"
"	border-radius:"
                        " 5px;\n"
"	padding: 5px;\n"
"	color: rgb(255, 170, 255);\n"
"}\n"
"QCommandLinkButton:hover {	\n"
"	color: rgb(255, 170, 255);\n"
"	background-color: rgb(44, 49, 60);\n"
"}\n"
"QCommandLinkButton:pressed {	\n"
"	color: rgb(189, 147, 249);\n"
"	background-color: rgb(52, 58, 71);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Button */\n"
"#pagesContainer QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"#pagesContainer QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"#pagesContainer QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}\n"
"\n"
"")
        self.horizontalLayout_9 = QHBoxLayout(self.styleSheet)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.bgApp = QFrame(self.styleSheet)
        self.bgApp.setObjectName(u"bgApp")
        self.bgApp.setStyleSheet(u"")
        self.bgApp.setFrameShape(QFrame.NoFrame)
        self.bgApp.setFrameShadow(QFrame.Raised)
        self.appLayout = QHBoxLayout(self.bgApp)
        self.appLayout.setSpacing(0)
        self.appLayout.setObjectName(u"appLayout")
        self.appLayout.setContentsMargins(0, 0, 0, 0)
        self.leftMenuBg = QFrame(self.bgApp)
        self.leftMenuBg.setObjectName(u"leftMenuBg")
        self.leftMenuBg.setMinimumSize(QSize(60, 0))
        self.leftMenuBg.setMaximumSize(QSize(200, 16777215))
        self.leftMenuBg.setFrameShape(QFrame.NoFrame)
        self.leftMenuBg.setFrameShadow(QFrame.Raised)
        self.topLogoInfo = QFrame(self.leftMenuBg)
        self.topLogoInfo.setObjectName(u"topLogoInfo")
        self.topLogoInfo.setGeometry(QRect(0, 0, 60, 50))
        self.topLogoInfo.setMinimumSize(QSize(0, 50))
        self.topLogoInfo.setMaximumSize(QSize(16777215, 50))
        self.topLogoInfo.setFrameShape(QFrame.NoFrame)
        self.topLogoInfo.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.topLogoInfo)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.topLogo = QFrame(self.topLogoInfo)
        self.topLogo.setObjectName(u"topLogo")
        self.topLogo.setMinimumSize(QSize(42, 52))
        self.topLogo.setMaximumSize(QSize(42, 52))
        self.topLogo.setStyleSheet(u"background: url(:/images/images/images/GESLogo_Cropped.png);\n"
"background-size: auto;")
        self.topLogo.setFrameShape(QFrame.NoFrame)
        self.topLogo.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_6.addWidget(self.topLogo)

        self.leftMenuFrame = QFrame(self.leftMenuBg)
        self.leftMenuFrame.setObjectName(u"leftMenuFrame")
        self.leftMenuFrame.setGeometry(QRect(0, 50, 200, 668))
        self.leftMenuFrame.setMinimumSize(QSize(200, 0))
        self.leftMenuFrame.setMaximumSize(QSize(200, 16777215))
        self.leftMenuFrame.setFrameShape(QFrame.NoFrame)
        self.leftMenuFrame.setFrameShadow(QFrame.Raised)
        self.verticalMenuLayout = QVBoxLayout(self.leftMenuFrame)
        self.verticalMenuLayout.setSpacing(0)
        self.verticalMenuLayout.setObjectName(u"verticalMenuLayout")
        self.verticalMenuLayout.setContentsMargins(0, 0, 0, 0)
        self.toggleBox = QFrame(self.leftMenuFrame)
        self.toggleBox.setObjectName(u"toggleBox")
        self.toggleBox.setMaximumSize(QSize(16777215, 45))
        self.toggleBox.setFrameShape(QFrame.NoFrame)
        self.toggleBox.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.toggleBox)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.toggleButton = QPushButton(self.toggleBox)
        self.toggleButton.setObjectName(u"toggleButton")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toggleButton.sizePolicy().hasHeightForWidth())
        self.toggleButton.setSizePolicy(sizePolicy)
        self.toggleButton.setMinimumSize(QSize(0, 45))
        self.toggleButton.setFont(font)
        self.toggleButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.toggleButton.setLayoutDirection(Qt.LeftToRight)
        self.toggleButton.setStyleSheet(u"background-image: url(:/icons/images/icons/icon_menu.png);")

        self.verticalLayout_4.addWidget(self.toggleButton)


        self.verticalMenuLayout.addWidget(self.toggleBox)

        self.topMenu = QFrame(self.leftMenuFrame)
        self.topMenu.setObjectName(u"topMenu")
        self.topMenu.setFrameShape(QFrame.NoFrame)
        self.topMenu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.topMenu)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.btn_home = QPushButton(self.topMenu)
        self.btn_home.setObjectName(u"btn_home")
        sizePolicy.setHeightForWidth(self.btn_home.sizePolicy().hasHeightForWidth())
        self.btn_home.setSizePolicy(sizePolicy)
        self.btn_home.setMinimumSize(QSize(0, 45))
        self.btn_home.setFont(font)
        self.btn_home.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_home.setLayoutDirection(Qt.LeftToRight)
        self.btn_home.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-home.png);")

        self.verticalLayout_8.addWidget(self.btn_home)

        self.btn_AddData = QPushButton(self.topMenu)
        self.btn_AddData.setObjectName(u"btn_AddData")
        sizePolicy.setHeightForWidth(self.btn_AddData.sizePolicy().hasHeightForWidth())
        self.btn_AddData.setSizePolicy(sizePolicy)
        self.btn_AddData.setMinimumSize(QSize(0, 45))
        self.btn_AddData.setFont(font)
        self.btn_AddData.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_AddData.setLayoutDirection(Qt.LeftToRight)
        self.btn_AddData.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-plus.png);")

        self.verticalLayout_8.addWidget(self.btn_AddData)

        self.btnGraphCollection = QPushButton(self.topMenu)
        self.btnGraphCollection.setObjectName(u"btnGraphCollection")
        sizePolicy.setHeightForWidth(self.btnGraphCollection.sizePolicy().hasHeightForWidth())
        self.btnGraphCollection.setSizePolicy(sizePolicy)
        self.btnGraphCollection.setMinimumSize(QSize(0, 45))
        self.btnGraphCollection.setFont(font)
        self.btnGraphCollection.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnGraphCollection.setLayoutDirection(Qt.LeftToRight)
        self.btnGraphCollection.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-image1.png);")

        self.verticalLayout_8.addWidget(self.btnGraphCollection)

        self.toggleLeftBox = QPushButton(self.topMenu)
        self.toggleLeftBox.setObjectName(u"toggleLeftBox")
        sizePolicy.setHeightForWidth(self.toggleLeftBox.sizePolicy().hasHeightForWidth())
        self.toggleLeftBox.setSizePolicy(sizePolicy)
        self.toggleLeftBox.setMinimumSize(QSize(0, 45))
        self.toggleLeftBox.setFont(font)
        self.toggleLeftBox.setCursor(QCursor(Qt.PointingHandCursor))
        self.toggleLeftBox.setLayoutDirection(Qt.LeftToRight)
        self.toggleLeftBox.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-chart.png);")

        self.verticalLayout_8.addWidget(self.toggleLeftBox)

        self.btn_export = QPushButton(self.topMenu)
        self.btn_export.setObjectName(u"btn_export")
        sizePolicy.setHeightForWidth(self.btn_export.sizePolicy().hasHeightForWidth())
        self.btn_export.setSizePolicy(sizePolicy)
        self.btn_export.setMinimumSize(QSize(0, 45))
        self.btn_export.setFont(font)
        self.btn_export.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_export.setLayoutDirection(Qt.LeftToRight)
        self.btn_export.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-share-boxed.png);")

        self.verticalLayout_8.addWidget(self.btn_export)

        self.btn_exit = QPushButton(self.topMenu)
        self.btn_exit.setObjectName(u"btn_exit")
        sizePolicy.setHeightForWidth(self.btn_exit.sizePolicy().hasHeightForWidth())
        self.btn_exit.setSizePolicy(sizePolicy)
        self.btn_exit.setMinimumSize(QSize(0, 45))
        self.btn_exit.setFont(font)
        self.btn_exit.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_exit.setLayoutDirection(Qt.LeftToRight)
        self.btn_exit.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-x.png);")

        self.verticalLayout_8.addWidget(self.btn_exit)


        self.verticalMenuLayout.addWidget(self.topMenu, 0, Qt.AlignTop)


        self.appLayout.addWidget(self.leftMenuBg)

        self.extraLeftBox = QFrame(self.bgApp)
        self.extraLeftBox.setObjectName(u"extraLeftBox")
        self.extraLeftBox.setMinimumSize(QSize(0, 0))
        self.extraLeftBox.setMaximumSize(QSize(0, 16777215))
        self.extraLeftBox.setFrameShape(QFrame.NoFrame)
        self.extraLeftBox.setFrameShadow(QFrame.Raised)
        self.extraColumLayout = QVBoxLayout(self.extraLeftBox)
        self.extraColumLayout.setSpacing(0)
        self.extraColumLayout.setObjectName(u"extraColumLayout")
        self.extraColumLayout.setContentsMargins(0, 0, 0, 0)
        self.extraTopBg = QFrame(self.extraLeftBox)
        self.extraTopBg.setObjectName(u"extraTopBg")
        self.extraTopBg.setMinimumSize(QSize(0, 50))
        self.extraTopBg.setMaximumSize(QSize(16777215, 50))
        self.extraTopBg.setFrameShape(QFrame.NoFrame)
        self.extraTopBg.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.extraTopBg)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.extraTopLayout = QGridLayout()
        self.extraTopLayout.setObjectName(u"extraTopLayout")
        self.extraTopLayout.setHorizontalSpacing(10)
        self.extraTopLayout.setVerticalSpacing(0)
        self.extraTopLayout.setContentsMargins(10, -1, 10, -1)
        self.extraIcon = QFrame(self.extraTopBg)
        self.extraIcon.setObjectName(u"extraIcon")
        self.extraIcon.setMinimumSize(QSize(20, 0))
        self.extraIcon.setMaximumSize(QSize(20, 20))
        self.extraIcon.setFrameShape(QFrame.NoFrame)
        self.extraIcon.setFrameShadow(QFrame.Raised)

        self.extraTopLayout.addWidget(self.extraIcon, 0, 0, 1, 1)

        self.extraLabel = QLabel(self.extraTopBg)
        self.extraLabel.setObjectName(u"extraLabel")
        self.extraLabel.setMinimumSize(QSize(150, 0))

        self.extraTopLayout.addWidget(self.extraLabel, 0, 1, 1, 1)

        self.extraCloseColumnBtn = QPushButton(self.extraTopBg)
        self.extraCloseColumnBtn.setObjectName(u"extraCloseColumnBtn")
        self.extraCloseColumnBtn.setMinimumSize(QSize(28, 28))
        self.extraCloseColumnBtn.setMaximumSize(QSize(28, 28))
        self.extraCloseColumnBtn.setCursor(QCursor(Qt.PointingHandCursor))
        icon = QIcon()
        icon.addFile(u":/icons/images/icons/icon_close.png", QSize(), QIcon.Normal, QIcon.Off)
        self.extraCloseColumnBtn.setIcon(icon)
        self.extraCloseColumnBtn.setIconSize(QSize(20, 20))

        self.extraTopLayout.addWidget(self.extraCloseColumnBtn, 0, 2, 1, 1)


        self.verticalLayout_5.addLayout(self.extraTopLayout)


        self.extraColumLayout.addWidget(self.extraTopBg)

        self.extraContent = QFrame(self.extraLeftBox)
        self.extraContent.setObjectName(u"extraContent")
        self.extraContent.setMinimumSize(QSize(0, 0))
        self.extraContent.setFrameShape(QFrame.NoFrame)
        self.extraContent.setFrameShadow(QFrame.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.extraContent)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 20)
        self.extraTopMenu = QFrame(self.extraContent)
        self.extraTopMenu.setObjectName(u"extraTopMenu")
        self.extraTopMenu.setMinimumSize(QSize(0, 0))
        self.extraTopMenu.setFrameShape(QFrame.NoFrame)
        self.extraTopMenu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_11 = QVBoxLayout(self.extraTopMenu)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.btn_pointCloud = QPushButton(self.extraTopMenu)
        self.btn_pointCloud.setObjectName(u"btn_pointCloud")
        sizePolicy.setHeightForWidth(self.btn_pointCloud.sizePolicy().hasHeightForWidth())
        self.btn_pointCloud.setSizePolicy(sizePolicy)
        self.btn_pointCloud.setMinimumSize(QSize(0, 45))
        self.btn_pointCloud.setFont(font)
        self.btn_pointCloud.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_pointCloud.setToolTipDuration(1000)
        self.btn_pointCloud.setLayoutDirection(Qt.LeftToRight)
        self.btn_pointCloud.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-layers.png);")
        self.btn_pointCloud.setIconSize(QSize(16, 16))

        self.verticalLayout_11.addWidget(self.btn_pointCloud)

        self.btn_heatMap = QPushButton(self.extraTopMenu)
        self.btn_heatMap.setObjectName(u"btn_heatMap")
        sizePolicy.setHeightForWidth(self.btn_heatMap.sizePolicy().hasHeightForWidth())
        self.btn_heatMap.setSizePolicy(sizePolicy)
        self.btn_heatMap.setMinimumSize(QSize(0, 45))
        self.btn_heatMap.setFont(font)
        self.btn_heatMap.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_heatMap.setToolTipDuration(1000)
        self.btn_heatMap.setLayoutDirection(Qt.LeftToRight)
        self.btn_heatMap.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-map.png);")

        self.verticalLayout_11.addWidget(self.btn_heatMap)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.verticalLayout_11.addItem(self.horizontalSpacer)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.btnResetContainer = QToolButton(self.extraTopMenu)
        self.btnResetContainer.setObjectName(u"btnResetContainer")
        self.btnResetContainer.setToolTipDuration(1000)
        self.btnResetContainer.setStyleSheet(u"background:rgb(255, 255, 255);")
        icon1 = QIcon()
        icon1.addFile(u":/icons/images/icons/refresh-ccw.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnResetContainer.setIcon(icon1)
        self.btnResetContainer.setArrowType(Qt.NoArrow)

        self.horizontalLayout_8.addWidget(self.btnResetContainer)

        self.lblGraphImages = QLabel(self.extraTopMenu)
        self.lblGraphImages.setObjectName(u"lblGraphImages")
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setItalic(False)
        font1.setUnderline(False)
        font1.setStrikeOut(False)
        self.lblGraphImages.setFont(font1)
        self.lblGraphImages.setAlignment(Qt.AlignCenter)
        self.lblGraphImages.setMargin(5)

        self.horizontalLayout_8.addWidget(self.lblGraphImages)


        self.verticalLayout_11.addLayout(self.horizontalLayout_8)


        self.verticalLayout_12.addWidget(self.extraTopMenu, 0, Qt.AlignTop)

        self.graphImagesContainer = QGraphicsView(self.extraContent)
        self.graphImagesContainer.setObjectName(u"graphImagesContainer")
        self.graphImagesContainer.setFocusPolicy(Qt.StrongFocus)
        self.graphImagesContainer.setAcceptDrops(False)
        self.graphImagesContainer.setStyleSheet(u"background: rgb(0, 0, 0);")

        self.verticalLayout_12.addWidget(self.graphImagesContainer)


        self.extraColumLayout.addWidget(self.extraContent)


        self.appLayout.addWidget(self.extraLeftBox)

        self.contentBox = QFrame(self.bgApp)
        self.contentBox.setObjectName(u"contentBox")
        self.contentBox.setFrameShape(QFrame.NoFrame)
        self.contentBox.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.contentBox)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.contentTopBg = QFrame(self.contentBox)
        self.contentTopBg.setObjectName(u"contentTopBg")
        self.contentTopBg.setMinimumSize(QSize(0, 50))
        self.contentTopBg.setMaximumSize(QSize(16777215, 50))
        self.contentTopBg.setFrameShape(QFrame.NoFrame)
        self.contentTopBg.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.contentTopBg)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 10, 0)
        self.leftBox = QFrame(self.contentTopBg)
        self.leftBox.setObjectName(u"leftBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.leftBox.sizePolicy().hasHeightForWidth())
        self.leftBox.setSizePolicy(sizePolicy1)
        self.leftBox.setFrameShape(QFrame.NoFrame)
        self.leftBox.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.leftBox)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.titleRightInfo = QLabel(self.leftBox)
        self.titleRightInfo.setObjectName(u"titleRightInfo")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.titleRightInfo.sizePolicy().hasHeightForWidth())
        self.titleRightInfo.setSizePolicy(sizePolicy2)
        self.titleRightInfo.setMaximumSize(QSize(16777215, 45))
        self.titleRightInfo.setFont(font)
        self.titleRightInfo.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.titleRightInfo)


        self.horizontalLayout.addWidget(self.leftBox)

        self.rightButtons = QFrame(self.contentTopBg)
        self.rightButtons.setObjectName(u"rightButtons")
        self.rightButtons.setMinimumSize(QSize(0, 28))
        self.rightButtons.setFrameShape(QFrame.NoFrame)
        self.rightButtons.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.rightButtons)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.settingsTopBtn = QPushButton(self.rightButtons)
        self.settingsTopBtn.setObjectName(u"settingsTopBtn")
        self.settingsTopBtn.setMinimumSize(QSize(28, 28))
        self.settingsTopBtn.setMaximumSize(QSize(28, 28))
        self.settingsTopBtn.setCursor(QCursor(Qt.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(u":/icons/images/icons/icon_settings.png", QSize(), QIcon.Normal, QIcon.Off)
        self.settingsTopBtn.setIcon(icon2)
        self.settingsTopBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.settingsTopBtn)

        self.minimizeAppBtn = QPushButton(self.rightButtons)
        self.minimizeAppBtn.setObjectName(u"minimizeAppBtn")
        self.minimizeAppBtn.setMinimumSize(QSize(28, 28))
        self.minimizeAppBtn.setMaximumSize(QSize(28, 28))
        self.minimizeAppBtn.setCursor(QCursor(Qt.PointingHandCursor))
        icon3 = QIcon()
        icon3.addFile(u":/icons/images/icons/icon_minimize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.minimizeAppBtn.setIcon(icon3)
        self.minimizeAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.minimizeAppBtn)

        self.maximizeRestoreAppBtn = QPushButton(self.rightButtons)
        self.maximizeRestoreAppBtn.setObjectName(u"maximizeRestoreAppBtn")
        self.maximizeRestoreAppBtn.setMinimumSize(QSize(28, 28))
        self.maximizeRestoreAppBtn.setMaximumSize(QSize(28, 28))
        font2 = QFont()
        font2.setFamilies([u"Segoe UI"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        font2.setStyleStrategy(QFont.PreferDefault)
        self.maximizeRestoreAppBtn.setFont(font2)
        self.maximizeRestoreAppBtn.setCursor(QCursor(Qt.PointingHandCursor))
        icon4 = QIcon()
        icon4.addFile(u":/icons/images/icons/icon_maximize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.maximizeRestoreAppBtn.setIcon(icon4)
        self.maximizeRestoreAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.maximizeRestoreAppBtn)

        self.closeAppBtn = QPushButton(self.rightButtons)
        self.closeAppBtn.setObjectName(u"closeAppBtn")
        self.closeAppBtn.setMinimumSize(QSize(28, 28))
        self.closeAppBtn.setMaximumSize(QSize(28, 28))
        self.closeAppBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.closeAppBtn.setIcon(icon)
        self.closeAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.closeAppBtn)


        self.horizontalLayout.addWidget(self.rightButtons, 0, Qt.AlignRight)


        self.verticalLayout_2.addWidget(self.contentTopBg)

        self.contentBottom = QFrame(self.contentBox)
        self.contentBottom.setObjectName(u"contentBottom")
        self.contentBottom.setFrameShape(QFrame.NoFrame)
        self.contentBottom.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.contentBottom)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.content = QFrame(self.contentBottom)
        self.content.setObjectName(u"content")
        self.content.setFrameShape(QFrame.NoFrame)
        self.content.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.content)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.pagesContainer = QFrame(self.content)
        self.pagesContainer.setObjectName(u"pagesContainer")
        self.pagesContainer.setStyleSheet(u"")
        self.pagesContainer.setFrameShape(QFrame.NoFrame)
        self.pagesContainer.setFrameShadow(QFrame.Raised)
        self.verticalLayout_15 = QVBoxLayout(self.pagesContainer)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(10, 10, 10, 10)
        self.stackedWidget = QStackedWidget(self.pagesContainer)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setStyleSheet(u"background: transparent;")
        self.home = QWidget()
        self.home.setObjectName(u"home")
        self.home.setStyleSheet(u"\n"
"background-position: center;\n"
"background-repeat: no-repeat;")
        self.verticalLayout_3 = QVBoxLayout(self.home)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.frame_2 = QFrame(self.home)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy2.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy2)
        self.frame_2.setStyleSheet(u"image: url(:/images/images/images/GESpanel.png);\n"
"\n"
"")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)

        self.verticalLayout_3.addWidget(self.frame_2)

        self.frame = QFrame(self.home)
        self.frame.setObjectName(u"frame")
        self.frame.setStyleSheet(u"")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.frame)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.btn_AddFile = QPushButton(self.frame)
        self.btn_AddFile.setObjectName(u"btn_AddFile")
        self.btn_AddFile.setMinimumSize(QSize(100, 100))
        self.btn_AddFile.setStyleSheet(u"")
        icon5 = QIcon()
        icon5.addFile(u":/images/images/images/folder.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_AddFile.setIcon(icon5)
        self.btn_AddFile.setIconSize(QSize(130, 150))

        self.horizontalLayout_10.addWidget(self.btn_AddFile)

        self.btn_PlotSurface = QPushButton(self.frame)
        self.btn_PlotSurface.setObjectName(u"btn_PlotSurface")
        icon6 = QIcon()
        icon6.addFile(u":/images/images/images/layer.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_PlotSurface.setIcon(icon6)
        self.btn_PlotSurface.setIconSize(QSize(130, 150))

        self.horizontalLayout_10.addWidget(self.btn_PlotSurface)

        self.btn_PlotHeatmap = QPushButton(self.frame)
        self.btn_PlotHeatmap.setObjectName(u"btn_PlotHeatmap")
        icon7 = QIcon()
        icon7.addFile(u":/images/images/images/map.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_PlotHeatmap.setIcon(icon7)
        self.btn_PlotHeatmap.setIconSize(QSize(130, 150))

        self.horizontalLayout_10.addWidget(self.btn_PlotHeatmap)

        self.btn_PDFeditor = QPushButton(self.frame)
        self.btn_PDFeditor.setObjectName(u"btn_PDFeditor")
        icon8 = QIcon()
        icon8.addFile(u":/images/images/images/photo-edit.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_PDFeditor.setIcon(icon8)
        self.btn_PDFeditor.setIconSize(QSize(130, 150))

        self.horizontalLayout_10.addWidget(self.btn_PDFeditor)


        self.verticalLayout_3.addWidget(self.frame, 0, Qt.AlignBottom)

        self.stackedWidget.addWidget(self.home)
        self.page_add_data = QWidget()
        self.page_add_data.setObjectName(u"page_add_data")
        self.page_add_data.setStyleSheet(u"b")
        self.verticalLayout = QVBoxLayout(self.page_add_data)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.row_1 = QFrame(self.page_add_data)
        self.row_1.setObjectName(u"row_1")
        self.row_1.setFrameShape(QFrame.StyledPanel)
        self.row_1.setFrameShadow(QFrame.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.row_1)
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.frame_div_content_1 = QFrame(self.row_1)
        self.frame_div_content_1.setObjectName(u"frame_div_content_1")
        self.frame_div_content_1.setMinimumSize(QSize(0, 110))
        self.frame_div_content_1.setMaximumSize(QSize(500, 110))
        self.frame_div_content_1.setFrameShape(QFrame.NoFrame)
        self.frame_div_content_1.setFrameShadow(QFrame.Raised)
        self.verticalLayout_16 = QVBoxLayout(self.frame_div_content_1)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.frame_title_wid_1 = QFrame(self.frame_div_content_1)
        self.frame_title_wid_1.setObjectName(u"frame_title_wid_1")
        self.frame_title_wid_1.setMaximumSize(QSize(16777215, 35))
        self.frame_title_wid_1.setFrameShape(QFrame.StyledPanel)
        self.frame_title_wid_1.setFrameShadow(QFrame.Raised)
        self.verticalLayout_18 = QVBoxLayout(self.frame_title_wid_1)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.labelBoxBlenderInstalation = QLabel(self.frame_title_wid_1)
        self.labelBoxBlenderInstalation.setObjectName(u"labelBoxBlenderInstalation")
        self.labelBoxBlenderInstalation.setFont(font)
        self.labelBoxBlenderInstalation.setStyleSheet(u"")

        self.verticalLayout_18.addWidget(self.labelBoxBlenderInstalation)


        self.verticalLayout_16.addWidget(self.frame_title_wid_1)

        self.frame_content_wid_1 = QFrame(self.frame_div_content_1)
        self.frame_content_wid_1.setObjectName(u"frame_content_wid_1")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.frame_content_wid_1.sizePolicy().hasHeightForWidth())
        self.frame_content_wid_1.setSizePolicy(sizePolicy3)
        self.frame_content_wid_1.setMinimumSize(QSize(0, 0))
        self.frame_content_wid_1.setFrameShape(QFrame.NoFrame)
        self.frame_content_wid_1.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_content_wid_1)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, -1, 0)
        self.btn_open = QPushButton(self.frame_content_wid_1)
        self.btn_open.setObjectName(u"btn_open")
        self.btn_open.setMinimumSize(QSize(120, 30))
        self.btn_open.setFont(font)
        self.btn_open.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_open.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        icon9 = QIcon()
        icon9.addFile(u":/icons/images/icons/cil-folder-open.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_open.setIcon(icon9)

        self.horizontalLayout_7.addWidget(self.btn_open)

        self.btn_removeData = QPushButton(self.frame_content_wid_1)
        self.btn_removeData.setObjectName(u"btn_removeData")
        self.btn_removeData.setMinimumSize(QSize(120, 30))
        self.btn_removeData.setFont(font)
        self.btn_removeData.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_removeData.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        icon10 = QIcon()
        icon10.addFile(u":/icons/images/icons/trash-2_disabled.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_removeData.setIcon(icon10)
        self.btn_removeData.setIconSize(QSize(18, 18))

        self.horizontalLayout_7.addWidget(self.btn_removeData)


        self.verticalLayout_16.addWidget(self.frame_content_wid_1)


        self.verticalLayout_10.addWidget(self.frame_div_content_1, 0, Qt.AlignTop)


        self.verticalLayout.addWidget(self.row_1)

        self.row_3 = QFrame(self.page_add_data)
        self.row_3.setObjectName(u"row_3")
        sizePolicy2.setHeightForWidth(self.row_3.sizePolicy().hasHeightForWidth())
        self.row_3.setSizePolicy(sizePolicy2)
        self.row_3.setMinimumSize(QSize(0, 150))
        self.row_3.setFrameShape(QFrame.StyledPanel)
        self.row_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.row_3)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.tableWidget = QTableWidget(self.row_3)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)

        self.verticalLayout_9.addWidget(self.tableWidget)


        self.verticalLayout.addWidget(self.row_3)

        self.stackedWidget.addWidget(self.page_add_data)
        self.new_page = QWidget()
        self.new_page.setObjectName(u"new_page")
        self.verticalLayout_20 = QVBoxLayout(self.new_page)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.pdfToolBox = QGroupBox(self.new_page)
        self.pdfToolBox.setObjectName(u"pdfToolBox")
        sizePolicy4 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.pdfToolBox.sizePolicy().hasHeightForWidth())
        self.pdfToolBox.setSizePolicy(sizePolicy4)
        self.pdfToolBox.setMinimumSize(QSize(495, 60))
        self.pdfToolBox.setMaximumSize(QSize(500, 60))
        self.pdfToolBox.setBaseSize(QSize(0, 0))
        self.pdfToolBox.setFlat(False)
        self.pdfToolBox.setCheckable(False)
        self.gridLayout_4 = QGridLayout(self.pdfToolBox)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(-1, 1, -1, -1)
        self.btnAddNewPage = QPushButton(self.pdfToolBox)
        self.btnAddNewPage.setObjectName(u"btnAddNewPage")
        self.btnAddNewPage.setMinimumSize(QSize(50, 30))
        self.btnAddNewPage.setMaximumSize(QSize(50, 30))
        icon11 = QIcon()
        icon11.addFile(u":/icons/images/icons/file-plus_disabled.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnAddNewPage.setIcon(icon11)
        self.btnAddNewPage.setIconSize(QSize(25, 25))

        self.gridLayout_4.addWidget(self.btnAddNewPage, 0, 4, 1, 1)

        self.btnSavePdf = QPushButton(self.pdfToolBox)
        self.btnSavePdf.setObjectName(u"btnSavePdf")
        self.btnSavePdf.setMinimumSize(QSize(50, 30))
        self.btnSavePdf.setMaximumSize(QSize(50, 30))
        icon12 = QIcon()
        icon12.addFile(u":/icons/images/icons/save_disabled.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnSavePdf.setIcon(icon12)
        self.btnSavePdf.setIconSize(QSize(25, 25))
        self.btnSavePdf.setFlat(False)

        self.gridLayout_4.addWidget(self.btnSavePdf, 0, 6, 1, 1)

        self.btnRemoveItem = QPushButton(self.pdfToolBox)
        self.btnRemoveItem.setObjectName(u"btnRemoveItem")
        sizePolicy4.setHeightForWidth(self.btnRemoveItem.sizePolicy().hasHeightForWidth())
        self.btnRemoveItem.setSizePolicy(sizePolicy4)
        self.btnRemoveItem.setMinimumSize(QSize(50, 30))
        self.btnRemoveItem.setMaximumSize(QSize(50, 30))
        icon13 = QIcon()
        icon13.addFile(u":/icons/images/icons/x_disabled.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnRemoveItem.setIcon(icon13)
        self.btnRemoveItem.setIconSize(QSize(25, 25))

        self.gridLayout_4.addWidget(self.btnRemoveItem, 0, 2, 1, 1)

        self.btnAddText = QPushButton(self.pdfToolBox)
        self.btnAddText.setObjectName(u"btnAddText")
        sizePolicy4.setHeightForWidth(self.btnAddText.sizePolicy().hasHeightForWidth())
        self.btnAddText.setSizePolicy(sizePolicy4)
        self.btnAddText.setMinimumSize(QSize(50, 30))
        self.btnAddText.setMaximumSize(QSize(50, 50))
        self.btnAddText.setFont(font)
        icon14 = QIcon()
        icon14.addFile(u":/icons/images/icons/type_disabled.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnAddText.setIcon(icon14)
        self.btnAddText.setIconSize(QSize(25, 25))

        self.gridLayout_4.addWidget(self.btnAddText, 0, 3, 1, 1)

        self.btnPan = QPushButton(self.pdfToolBox)
        self.btnPan.setObjectName(u"btnPan")
        sizePolicy4.setHeightForWidth(self.btnPan.sizePolicy().hasHeightForWidth())
        self.btnPan.setSizePolicy(sizePolicy4)
        self.btnPan.setMinimumSize(QSize(50, 30))
        self.btnPan.setMaximumSize(QSize(50, 30))
        icon15 = QIcon()
        icon15.addFile(u":/icons/images/icons/move_disabled.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnPan.setIcon(icon15)
        self.btnPan.setIconSize(QSize(25, 25))

        self.gridLayout_4.addWidget(self.btnPan, 0, 1, 1, 1)

        self.btnNewPage = QPushButton(self.pdfToolBox)
        self.btnNewPage.setObjectName(u"btnNewPage")
        self.btnNewPage.setMinimumSize(QSize(50, 30))
        self.btnNewPage.setMaximumSize(QSize(50, 30))
        icon16 = QIcon()
        icon16.addFile(u":/icons/images/icons/file_disabled.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnNewPage.setIcon(icon16)
        self.btnNewPage.setIconSize(QSize(25, 25))

        self.gridLayout_4.addWidget(self.btnNewPage, 0, 5, 1, 1)

        self.btnSelect = QPushButton(self.pdfToolBox)
        self.btnSelect.setObjectName(u"btnSelect")
        sizePolicy4.setHeightForWidth(self.btnSelect.sizePolicy().hasHeightForWidth())
        self.btnSelect.setSizePolicy(sizePolicy4)
        self.btnSelect.setMinimumSize(QSize(50, 30))
        self.btnSelect.setMaximumSize(QSize(50, 50))
        self.btnSelect.setStyleSheet(u"background: #d9bceb;")
        icon17 = QIcon()
        icon17.addFile(u":/icons/images/icons/mouse-pointer_focus.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnSelect.setIcon(icon17)
        self.btnSelect.setIconSize(QSize(25, 25))

        self.gridLayout_4.addWidget(self.btnSelect, 0, 0, 1, 1)


        self.verticalLayout_20.addWidget(self.pdfToolBox, 0, Qt.AlignHCenter|Qt.AlignTop)

        self.graphicsView = CustomGraphicsView(self.new_page)
        self.graphicsView.setObjectName(u"graphicsView")
        sizePolicy5 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy5)
        self.graphicsView.setMaximumSize(QSize(1000000, 10000000))

        self.verticalLayout_20.addWidget(self.graphicsView, 0, Qt.AlignHCenter)

        self.stackedWidget.addWidget(self.new_page)
        self.graph_collection = QWidget()
        self.graph_collection.setObjectName(u"graph_collection")
        self.gridLayout_2 = QGridLayout(self.graph_collection)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.graphTable = QTableWidget(self.graph_collection)
        self.graphTable.setObjectName(u"graphTable")

        self.gridLayout_2.addWidget(self.graphTable, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.graph_collection)
        self.line_graph = QWidget()
        self.line_graph.setObjectName(u"line_graph")
        self.gridLayout_3 = QGridLayout(self.line_graph)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.line_graph_placeholder = MplGraph(self.line_graph)
        self.line_graph_placeholder.setObjectName(u"line_graph_placeholder")

        self.gridLayout_3.addWidget(self.line_graph_placeholder, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.line_graph)
        self.heat_map = QWidget()
        self.heat_map.setObjectName(u"heat_map")
        self.stackedWidget.addWidget(self.heat_map)

        self.verticalLayout_15.addWidget(self.stackedWidget)


        self.horizontalLayout_4.addWidget(self.pagesContainer)

        self.extraRightBox = QFrame(self.content)
        self.extraRightBox.setObjectName(u"extraRightBox")
        self.extraRightBox.setMinimumSize(QSize(0, 0))
        self.extraRightBox.setMaximumSize(QSize(0, 16777215))
        self.extraRightBox.setFrameShape(QFrame.NoFrame)
        self.extraRightBox.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.extraRightBox)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.themeSettingsTopDetail = QFrame(self.extraRightBox)
        self.themeSettingsTopDetail.setObjectName(u"themeSettingsTopDetail")
        self.themeSettingsTopDetail.setMaximumSize(QSize(16777215, 3))
        self.themeSettingsTopDetail.setFrameShape(QFrame.NoFrame)
        self.themeSettingsTopDetail.setFrameShadow(QFrame.Raised)

        self.verticalLayout_7.addWidget(self.themeSettingsTopDetail)

        self.contentSettings = QFrame(self.extraRightBox)
        self.contentSettings.setObjectName(u"contentSettings")
        self.contentSettings.setLayoutDirection(Qt.LeftToRight)
        self.contentSettings.setFrameShape(QFrame.NoFrame)
        self.contentSettings.setFrameShadow(QFrame.Raised)
        self.verticalLayout_13 = QVBoxLayout(self.contentSettings)
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.groupBox = QGroupBox(self.contentSettings)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMinimumSize(QSize(0, 0))
        self.groupBox.setMaximumSize(QSize(16777215, 170))
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.gridLayout_5.addWidget(self.label, 0, 0, 1, 1, Qt.AlignTop)

        self.cbFillHole = QCheckBox(self.groupBox)
        self.cbFillHole.setObjectName(u"cbFillHole")
        self.cbFillHole.setCheckable(False)
        self.cbFillHole.setTristate(False)

        self.gridLayout_5.addWidget(self.cbFillHole, 3, 0, 1, 1)

        self.leVariance = QLineEdit(self.groupBox)
        self.leVariance.setObjectName(u"leVariance")
        self.leVariance.setMinimumSize(QSize(0, 20))
        self.leVariance.setMaximumSize(QSize(16777215, 25))
        self.leVariance.setReadOnly(True)

        self.gridLayout_5.addWidget(self.leVariance, 1, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_2, 2, 0, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_5, 0, 0, 1, 1)

        self.btnSaveParams = QPushButton(self.groupBox)
        self.btnSaveParams.setObjectName(u"btnSaveParams")
        self.btnSaveParams.setMinimumSize(QSize(0, 30))
        self.btnSaveParams.setLayoutDirection(Qt.LeftToRight)
        self.btnSaveParams.setStyleSheet(u"background-color:rgb(85, 0, 127);")
        icon18 = QIcon()
        icon18.addFile(u":/icons/images/icons/cil-pencil.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnSaveParams.setIcon(icon18)

        self.gridLayout.addWidget(self.btnSaveParams, 1, 0, 1, 1)


        self.verticalLayout_13.addWidget(self.groupBox)

        self.topMenus = QFrame(self.contentSettings)
        self.topMenus.setObjectName(u"topMenus")
        self.topMenus.setFrameShape(QFrame.NoFrame)
        self.topMenus.setFrameShadow(QFrame.Raised)
        self.verticalLayout_14 = QVBoxLayout(self.topMenus)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_13.addWidget(self.topMenus, 0, Qt.AlignTop)


        self.verticalLayout_7.addWidget(self.contentSettings)


        self.horizontalLayout_4.addWidget(self.extraRightBox)


        self.verticalLayout_6.addWidget(self.content)

        self.bottomBar = QFrame(self.contentBottom)
        self.bottomBar.setObjectName(u"bottomBar")
        self.bottomBar.setMinimumSize(QSize(0, 22))
        self.bottomBar.setMaximumSize(QSize(16777215, 22))
        self.bottomBar.setFrameShape(QFrame.NoFrame)
        self.bottomBar.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.bottomBar)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.progressLabel = QLabel(self.bottomBar)
        self.progressLabel.setObjectName(u"progressLabel")
        self.progressLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.progressLabel)

        self.progressBar = QProgressBar(self.bottomBar)
        self.progressBar.setObjectName(u"progressBar")
        sizePolicy6 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy6)
        self.progressBar.setMaximumSize(QSize(300, 16777215))
        self.progressBar.setStyleSheet(u"")
        self.progressBar.setValue(24)
        self.progressBar.setTextVisible(True)
        self.progressBar.setInvertedAppearance(False)

        self.horizontalLayout_5.addWidget(self.progressBar)

        self.creditsLabel = QLabel(self.bottomBar)
        self.creditsLabel.setObjectName(u"creditsLabel")
        sizePolicy7 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.creditsLabel.sizePolicy().hasHeightForWidth())
        self.creditsLabel.setSizePolicy(sizePolicy7)
        self.creditsLabel.setMaximumSize(QSize(100, 16))
        font3 = QFont()
        font3.setFamilies([u"Segoe UI"])
        font3.setBold(False)
        font3.setItalic(False)
        self.creditsLabel.setFont(font3)
        self.creditsLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.creditsLabel)

        self.version = QLabel(self.bottomBar)
        self.version.setObjectName(u"version")
        sizePolicy7.setHeightForWidth(self.version.sizePolicy().hasHeightForWidth())
        self.version.setSizePolicy(sizePolicy7)
        self.version.setMaximumSize(QSize(50, 16777215))
        self.version.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.version)

        self.frame_size_grip = QFrame(self.bottomBar)
        self.frame_size_grip.setObjectName(u"frame_size_grip")
        self.frame_size_grip.setMinimumSize(QSize(20, 0))
        self.frame_size_grip.setMaximumSize(QSize(20, 16777215))
        self.frame_size_grip.setFrameShape(QFrame.NoFrame)
        self.frame_size_grip.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_5.addWidget(self.frame_size_grip)


        self.verticalLayout_6.addWidget(self.bottomBar)


        self.verticalLayout_2.addWidget(self.contentBottom)


        self.appLayout.addWidget(self.contentBox)


        self.horizontalLayout_9.addWidget(self.bgApp)

        MainWindow.setCentralWidget(self.styleSheet)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)
        self.btnSavePdf.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.toggleButton.setText(QCoreApplication.translate("MainWindow", u"Hide", None))
        self.btn_home.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.btn_AddData.setText(QCoreApplication.translate("MainWindow", u"Add data", None))
        self.btnGraphCollection.setText(QCoreApplication.translate("MainWindow", u"Graph collection", None))
        self.toggleLeftBox.setText(QCoreApplication.translate("MainWindow", u"Visualize data", None))
        self.btn_export.setText(QCoreApplication.translate("MainWindow", u"PDF Editor", None))
        self.btn_exit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.extraLabel.setText(QCoreApplication.translate("MainWindow", u"Graph generators", None))
#if QT_CONFIG(tooltip)
        self.extraCloseColumnBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Close left box", None))
#endif // QT_CONFIG(tooltip)
        self.extraCloseColumnBtn.setText("")
#if QT_CONFIG(tooltip)
        self.btn_pointCloud.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.btn_pointCloud.setText(QCoreApplication.translate("MainWindow", u"Surface graph", None))
#if QT_CONFIG(tooltip)
        self.btn_heatMap.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.btn_heatMap.setText(QCoreApplication.translate("MainWindow", u"HeatMap", None))
#if QT_CONFIG(tooltip)
        self.btnResetContainer.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.btnResetContainer.setText("")
        self.lblGraphImages.setText(QCoreApplication.translate("MainWindow", u"Graph Images", None))
        self.titleRightInfo.setText(QCoreApplication.translate("MainWindow", u"HeatMap Generator", None))
#if QT_CONFIG(tooltip)
        self.settingsTopBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Settings", None))
#endif // QT_CONFIG(tooltip)
        self.settingsTopBtn.setText("")
#if QT_CONFIG(tooltip)
        self.minimizeAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Minimize", None))
#endif // QT_CONFIG(tooltip)
        self.minimizeAppBtn.setText("")
#if QT_CONFIG(tooltip)
        self.maximizeRestoreAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Maximize", None))
#endif // QT_CONFIG(tooltip)
        self.maximizeRestoreAppBtn.setText("")
#if QT_CONFIG(tooltip)
        self.closeAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Close", None))
#endif // QT_CONFIG(tooltip)
        self.closeAppBtn.setText("")
#if QT_CONFIG(tooltip)
        self.btn_AddFile.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Add new data file</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.btn_AddFile.setText("")
#if QT_CONFIG(tooltip)
        self.btn_PlotSurface.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Render Surface Map</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.btn_PlotSurface.setText("")
#if QT_CONFIG(tooltip)
        self.btn_PlotHeatmap.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Render Heatmap</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.btn_PlotHeatmap.setText("")
#if QT_CONFIG(tooltip)
        self.btn_PDFeditor.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>PDF report editor</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.btn_PDFeditor.setText("")
        self.labelBoxBlenderInstalation.setText(QCoreApplication.translate("MainWindow", u"Select file contain x,y,z datas", None))
        self.btn_open.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.btn_removeData.setText(QCoreApplication.translate("MainWindow", u"Remove", None))
        self.pdfToolBox.setTitle(QCoreApplication.translate("MainWindow", u"ToolBox", None))
        self.btnAddNewPage.setText("")
        self.btnSavePdf.setText("")
        self.btnRemoveItem.setText("")
        self.btnAddText.setText("")
        self.btnPan.setText("")
        self.btnNewPage.setText("")
        self.btnSelect.setText("")
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Parameters", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Variance", None))
        self.cbFillHole.setText(QCoreApplication.translate("MainWindow", u"Fill Hole", None))
        self.btnSaveParams.setText(QCoreApplication.translate("MainWindow", u"Modify", None))
        self.progressLabel.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.creditsLabel.setText(QCoreApplication.translate("MainWindow", u"GES Vietnam", None))
        self.version.setText(QCoreApplication.translate("MainWindow", u"v1.0.0", None))
    # retranslateUi

