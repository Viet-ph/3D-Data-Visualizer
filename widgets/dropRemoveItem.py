from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QRectF, QPoint, QSize
from PySide6.QtGui import QPainter, QBrush, QColor

class XMarkItem(QGraphicsItem):
    def __init__(self, x, y, size):
        super().__init__()
        # self.rect = QRectF(x, y, size, size)
        self.setAcceptDrops(True)
        self.setPos(x, y)
        self.size = size
        self.backGroundColor = QColor(Qt.GlobalColor.lightGray)
        self.borderColor = Qt.GlobalColor.darkGray
        print(self.boundingRect())
        
    def boundingRect(self):
        return QRectF(QPoint(0, 0), QSize(self.size, self.size))  # Bounding rectangle of the X mark

    def paint(self, painter, option, widget):
        painter.setRenderHint(QPainter.Antialiasing)
        brush = painter.background()
        self.backGroundColor.setAlphaF(0.4)    
        brush.setColor(self.backGroundColor)
        pen = painter.pen()
        pen.setColor(self.borderColor)
        pen.setWidth(1)
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawEllipse(self.boundingRect().center(), self.size, self.size)
        painter.drawLine(self.boundingRect().topLeft(), self.boundingRect().bottomRight())  # Draw the diagonal from top-left to bottom-right
        painter.drawLine(self.boundingRect().bottomLeft(), self.boundingRect().topRight())  # Draw the diagonal from bottom-left to top-right

