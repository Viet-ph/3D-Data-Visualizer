from typing import Literal
from PySide6.QtWidgets import*
from PySide6.QtCore import *
from PySide6.QtGui import *
from .graphicsGlobal import isOperatingWith

class DraggableImageForPDF(QGraphicsPixmapItem):
    def __init__(self, x, y, callbackOnItemMoved=None, imgPath=None):
        super().__init__()
        self.setPos(x, y)
        self.imageFilePath = imgPath
        self.setPixmap(QPixmap(imgPath)
                       .scaledToWidth(350, Qt.TransformationMode.SmoothTransformation))
        self.setAcceptHoverEvents(True)
        self.setAcceptTouchEvents(True)
        self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable
                        | QGraphicsItem.GraphicsItemFlag.ItemIsSelectable
                        | self.flags())
        self.itemMoved = callbackOnItemMoved

    def resizeToPrintResolution(self):
        self.setPos(self.pos().x() * 3.125, self.pos().y() * 3.125)
        self.setPixmap(QPixmap(self.imageFilePath)
                       .scaledToWidth(350*3.125, Qt.TransformationMode.SmoothTransformation))
    
    def resizeToDisplayResolution(self):
        self.setPos(self.pos().x() / 3.125, self.pos().y() / 3.125)
        self.setPixmap(QPixmap(self.imageFilePath)
                       .scaledToWidth(350, Qt.TransformationMode.SmoothTransformation))

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        if (isOperatingWith("pan") or isOperatingWith("remove")):
            self.setCursor(Qt.CursorShape.OpenHandCursor)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.setCursor(Qt.CursorShape.ArrowCursor)

    def mousePressEvent(self, event):
        if isOperatingWith("pan") and event.button() == Qt.LeftButton:
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
            self.setOpacity(0.7)
        elif isOperatingWith("remove") and event.button() == Qt.LeftButton:
            self.setOpacity(0.7)
        else:
            return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if isOperatingWith("pan"):
            self.handleWhenMove(event)
        elif isOperatingWith("remove"):
            self.handleWhenDrag(event)
        else:
            return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if (isOperatingWith("pan")):
            self.setCursor(Qt.CursorShape.OpenHandCursor)
            newPosRoundedX =  20 *round(float(self.pos().x() / 20))
            newPosRoundedY =  20 *round(float(self.pos().y() / 20))

            self.setPos(newPosRoundedX, newPosRoundedY)
        print("Image mouse release called")
        self.setOpacity(1)
        return super().mouseReleaseEvent(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Delete:
            self.scene().removeItem(self)
        return super().keyPressEvent(event)
    
    def focusInEvent(self, event: QFocusEvent) -> None:
        return super().focusInEvent(event)
    
    def handleWhenMove(self, event:QGraphicsSceneMouseEvent):
        newPos = self.scenePos() + event.scenePos() - event.lastScenePos()
        if newPos.x() <= 1:
            newPos = QPointF(1, newPos.y())
        if newPos.y() <= 1: 
            newPos = QPointF(newPos.x(), 1)
        if newPos.x() + self.pixmap().size().width() >= self.scene().width():
            newPos = QPointF(self.scene().width() - self.pixmap().size().width(), newPos.y())
        if newPos.y() + self.pixmap().size().height() >= self.scene().height():
            newPos = QPointF(newPos.x(), self.scene().height() - self.pixmap().size().height())
        self.setPos(newPos.x(), newPos.y())
        self.itemMoved(self)

    def handleWhenDrag(self, event: QGraphicsSceneMouseEvent):
        drag = QDrag(event.widget())
        mimeData = QMimeData()
        mimeData.setProperty("reference", self)
        drag.setMimeData(mimeData)
        
        pixmap = QPixmap(80, 80)

        painter = QPainter(pixmap)
        painter.fillRect(pixmap.rect(), self.pixmap().scaled(80, 80))
        painter.end()

        drag.setPixmap(pixmap)
        drag.exec(Qt.DropAction.CopyAction | Qt.DropAction.MoveAction)


class DraggableImageForImageContainer(QGraphicsPixmapItem):
    def __init__(self, index, image: QLabel, imageName, callbackOnItemRemoved=None):
        super().__init__()
        self.margin = 15
        self.setToolTip(imageName)
        self.setPixmap(image.pixmap().scaled(QSize(190, 120), Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.setPos(5, (self.pixmap().height() + self.margin) * index + self.margin)
        self.setAcceptHoverEvents(True)
        self.setAcceptTouchEvents(True)
        self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable
                        | QGraphicsItem.GraphicsItemFlag.ItemIsSelectable
                        | self.flags())
        self.imageName = imageName
        self.itemRemoved = callbackOnItemRemoved
        
    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.setCursor(Qt.CursorShape.OpenHandCursor)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.setCursor(Qt.CursorShape.ArrowCursor)

    def mousePressEvent(self, event):
        # if isOperatingWith("pan") and event.button() == Qt.LeftButton:
        self.setCursor(Qt.CursorShape.ClosedHandCursor)
        self.setOpacity(0.7)
        # elif isOperatingWith("remove") and event.button() == Qt.LeftButton:
        #     self.setOpacity(0.7)
        # else:
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.handleWhenDrag(event)
        return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        # if (isOperatingWith("pan")):
        #     self.setCursor(Qt.CursorShape.OpenHandCursor)
        #     newPosRoundedX =  20 *round(float(self.pos().x() / 20))
        #     newPosRoundedY =  20 *round(float(self.pos().y() / 20))
        #     self.setPos(newPosRoundedX, newPosRoundedY)
        self.setCursor(Qt.CursorShape.OpenHandCursor)
        self.setOpacity(1)
        return super().mouseReleaseEvent(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Delete:
            self.scene().removeItem(self)
            self.itemRemoved(self.scenePos().y())
        return super().keyPressEvent(event)
    
    def focusInEvent(self, event: QFocusEvent) -> None:
        return super().focusInEvent(event)

    def handleWhenDrag(self, event: QGraphicsSceneMouseEvent):
        self.setOpacity(1)
        drag = QDrag(event.widget())
        mimeData = QMimeData()
        # mimeData.setProperty("reference", self)
        mimeData.setProperty("name", self.imageName)
        url = QUrl.fromLocalFile("PlotImages/" + self.imageName + ".png")
        mimeData.setUrls([url])
        #mimeData.setImageData(self.pixmap().scaledToWidth(250))
        drag.setMimeData(mimeData)

        pixmap = QPixmap(80, 80)

        painter = QPainter(pixmap)
        painter.fillRect(pixmap.rect(), self.pixmap().scaled(80, 80))
        painter.end()

        drag.setPixmap(pixmap)
        drag.exec(Qt.DropAction.CopyAction | Qt.DropAction.MoveAction)