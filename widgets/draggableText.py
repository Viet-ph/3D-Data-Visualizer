from PySide6.QtWidgets import*
from PySide6.QtCore import *
from PySide6.QtGui import *
from .graphicsGlobal import isOperatingWith

class Draggabletext(QGraphicsTextItem):
    itemMoved = Signal(QGraphicsTextItem)
    def __init__(self, x, y):
        super().__init__()
        self.setPos(x, y)
        self.setPlainText("Enter your text here")
        self.setAcceptTouchEvents(True)
        self.setAcceptHoverEvents(True)   
        font = QFont()
        font.setPixelSize(15)
        self.setFont(font)
        self.setTextInteractionFlags(Qt.TextInteractionFlag.TextEditorInteraction |
                                     self.textInteractionFlags())
                                        #  | Qt.TextInteractionFlag.TextSelectableByMouse
                                        #  | Qt.TextInteractionFlag.TextSelectableByKeyboard
                                        #  | Qt.TextInteractionFlag.TextBrowserInteraction)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable
                        | QGraphicsItem.GraphicsItemFlag.ItemIsSelectable
                        | self.flags())

    def resizeToPrintResolution(self):
        self.setPos(self.pos().x() * 3.125, self.pos().y() * 3.125)
        font = QFont()
        font.setPixelSize(self.font().pixelSize() * 3.12)
        self.setFont(font)
        

    def resizeToDisplayResolution(self):
        self.setPos(self.pos().x() / 3.125, self.pos().y() / 3.125)
        font = QFont()
        font.setPixelSize(self.font().pixelSize() / 3.12)
        self.setFont(font)

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        if (isOperatingWith("pan") or isOperatingWith("remove")):
            self.setCursor(Qt.CursorShape.OpenHandCursor)
   
    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Delete:
            self.scene().removeItem(self)
        return super().keyPressEvent(event)
    
    def mousePressEvent(self, event):
        if isOperatingWith("pan") and event.button() == Qt.LeftButton:
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
            self.setOpacity(0.7)
        elif isOperatingWith("remove"):
            self.setOpacity(0.7)
        else:
            return super().mouseMoveEvent(event)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if isOperatingWith("pan"):
            self.handleWhenMove(event)
        elif isOperatingWith("remove"):
            self.handleWhenDrag(event)

    def mouseReleaseEvent(self, event):
        print("Text mouse release called")
        if (isOperatingWith("pan")):
            self.setCursor(Qt.CursorShape.OpenHandCursor)
            newPosRoundedX =  20 *round(float(self.pos().x() / 20))
            newPosRoundedY =  20 *round(float(self.pos().y() / 20))
            self.setPos(newPosRoundedX, newPosRoundedY)

        self.setOpacity(1)

    def handleWhenMove(self, event:QGraphicsSceneMouseEvent):
        print("text scene width:",self.scene().width())
        newPos = self.scenePos() + event.scenePos() - event.lastScenePos()
        if newPos.x() <= 1:
            newPos = QPointF(1, newPos.y())
        if newPos.y() <= 1: 
            newPos = QPointF(newPos.x(), 1)
        if newPos.x() + self.boundingRect().width() >= self.scene().width():
            newPos = QPointF(self.scene().width() - self.boundingRect().width(), newPos.y())
        if newPos.y() + self.boundingRect().height() >= self.scene().height():
            newPos = QPointF(newPos.x(), self.scene().height() - self.boundingRect().height())
        self.itemMoved.emit(self)
        self.setPos(newPos)        

    def handleWhenDrag(self, event: QGraphicsSceneMouseEvent):
        drag = QDrag(self)
        mimeData = QMimeData()
        mimeData.setText(self.toPlainText())
        mimeData.setProperty("reference", self)
        drag.setMimeData(mimeData)
        
        pixmap = QPixmap(self.boundingRect().width(), self.boundingRect().height())
        pixmap.fill("#dfe8f0")

        painter = QPainter(pixmap)
        self.document().drawContents(painter, self.boundingRect())
        painter.end()

        print(self.sceneBoundingRect())
        drag.setPixmap(pixmap)
        drag.setHotSpot(QPoint(int(event.pos().x()), int(event.pos().y())))
        drag.exec(Qt.DropAction.CopyAction | Qt.DropAction.MoveAction)


