from typing import Optional
import PySide6.QtCore
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import PySide6.QtWidgets
import numpy as np

class Ruler(QWidget):
    sizeChanged = Signal(QSize)
    def __init__(self, parent:QAbstractScrollArea) -> None:
        super().__init__(parent)
        self.offset = 0
        #self.scrollBar = QScrollBar(self)
        parent.verticalScrollBar().valueChanged.connect(self.setOffset)
        parent.horizontalScrollBar().valueChanged.connect(self.setOffset)
        # self.scrollBar.valueChanged.connect(self.setOffset)
        # height = parent.height()
        self.setFixedWidth(40)
        self.setFixedHeight(1200)
        self.move(0, 40)
        self.setStyleSheet('background-color: #000000')


    def setOffset(self, value):
        self.offset = value
        self.repaint()
        #self.paintEvent(QPaintEvent(QRect()))

    @staticmethod
    def toMM():
        return 10 / QGuiApplication.primaryScreen().logicalDotsPerInchY()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.translate(0, - self.offset)
        heightMM = self.height() * Ruler.toMM()
        painter.setFont(self.font())
        painter.setPen(Qt.darkGray)
        fm = QFontMetrics(self.font())
        for position in np.arange(0, heightMM, 1):
            positionInPix = int(position / self.toMM())
            width = self.width()
            if position % 10 == 0:
                if position != 0:
                    txt = str(int(position))
                    txtRect = fm.boundingRect(txt).translated(0, positionInPix)
                    txtRect.translate(1, txtRect.height()/2)
                    painter.drawText(txtRect, txt)
                painter.drawLine(width - 20, positionInPix, width, positionInPix)
            else:
                painter.drawLine(width - 15, positionInPix, width, positionInPix)

    def resizeEvent(self, event):
        maximumMM = event.size().height() * Ruler.toMM()
        fm = QFontMetrics(self.font())
        w = fm.horizontalAdvance(str(maximumMM)) + 20
        if w != event.size().width():
            newSize = QSize(w, event.size().height())
            self.sizeChanged.emit(newSize)
            return self.setFixedSize(newSize)

        return super().resizeEvent(event)
    




    
        