from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from .graphicsGlobal import isOperatingWith
from .draggableImage import DraggableImageForPDF
from .draggableText import Draggabletext
from .dropRemoveItem import XMarkItem

class CustomGraphicsView(QGraphicsView):

    def __init__(self, parent):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.graphicScene = QGraphicsScene(self)
        self.setScene(self.graphicScene)
        self.graphicScene.setFocusOnTouch(True)
        self.graphicScene.setSceneRect(0, 0, 794, 1123)
        #self.setSceneRect(0, 0, 794, 1123)
        self.pageCount = 1
        self.pageHeight = 1123
        self.textBoxSelecting = False
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        # self.ruler = Ruler(self)
        # self.ruler.sizeChanged.connect(lambda size: self.setViewportMargins(size.width(), size.width(), 0, 0))
        self.setStyleSheet('background : #ffffff')
        print("Scene rect: ", self.sceneRect())

    # def setScene(self, scene: QGraphicsScene) -> None:https://www.copperspice.com/docs/cs_api/class_qgraphicsscene.html
    #     super().setScene(scene)

    #     if scene:
    #         self.ruler.setFixedWidth(scene.height())


    def drawBackground(self, painter: QPainter, rect: QRectF):
        # Call the base class implementation to draw the standard background
        super().drawBackground(painter, rect)
        # Set grid properties
        gridSpacing = 20  # Set the spacing between grid lines
        gridColor = '#acad9e'

        # Draw the grid
        left = int(rect.left()) - int(rect.left()) % gridSpacing
        top = int(rect.top()) - int(rect.top()) % gridSpacing
        lines = []

        # Generate vertical grid lines
        x = left
        while x < rect.right():
            lines.append((x, rect.top(), x, rect.bottom()))
            x += gridSpacing

        # Generate horizontal grid lines
        y = top
        while y < rect.bottom():
            lines.append((rect.left(), y, rect.right(), y))
            y += gridSpacing

        if (isOperatingWith("pan")):
            # Set grid line color and draw the lines
            painter.setPen(gridColor)
            for line in lines:
                painter.drawLine(*line)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasImage: 
            event.accept()
        else:
            event.ignore()
    
    def dragMoveEvent(self, event: QDragMoveEvent) -> None:
        if event.mimeData().hasImage: 
            event.accept()
            if isOperatingWith("remove"): 
                self.displayDropRemoveArea(event)
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent) -> None:
        item = event.mimeData().property("reference")
        if event.mimeData().hasImage: 
            event.setDropAction(Qt.DropAction.CopyAction)
            if isOperatingWith("normal") or isOperatingWith("pan"):
                if not self.isItemInScene(item):                         
                    self.insertImageItem(event)
            elif isOperatingWith("remove"):
                self.removeItem(event)

        if item: item.setOpacity(1)
        return super().dropEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        #super().mouseReleaseEvent(event)
        if self.textBoxSelecting:
            self.insertTextItem(event.pos().x(), event.pos().y())
            self.viewport().setCursor(Qt.CursorShape.ArrowCursor)
            self.textBoxSelecting = False
        return super().mouseReleaseEvent(event)

    def insertImageItem(self, event: QDropEvent):
        image = None
        try:
            filePath = event.mimeData().urls()[0].toLocalFile()
            image = DraggableImageForPDF(event.pos().x(),
                                    event.pos().y() + self.verticalScrollBar().sliderPosition(), 
                                    self.itemMovedHandler,
                                    filePath)
            imageName = filePath.split('/')[-1].removesuffix('.png')
            self.insertTextItem(image.scenePos().x(),
                                image.pos().y() + image.boundingRect().height() + 5,
                                imageName)
        except IndexError:
            pass 
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            return
        
        self.graphicScene.addItem(image)

    def prepareToAddtextItem(self):
        if (isOperatingWith("normal")):
            self.textBoxSelecting = True
            self.viewport().setCursor(Qt.CursorShape.IBeamCursor)

    def insertTextItem(self, x, y, plainText=None):
        textBox = Draggabletext(x, y)
        self.graphicScene.addItem(textBox)
        textBox.itemMoved.connect(self.itemMovedHandler)
        if plainText: textBox.setPlainText(plainText)

    def removeItem(self, event: QDropEvent):
        dropRemoveSection = self.graphicScene.items()[-1]
        dropRemoveSection.hide()
        dropRemoveSection.backGroundColor = QColor(Qt.GlobalColor.gray)
        dropRemoveSection.borderColor = Qt.GlobalColor.darkGray
                
        victim = event.mimeData().property("reference")
        if (self.isInDropArea(event)):
            self.graphicScene.removeItem(victim)

    def isInDropArea(self, event):
        dropRemoveSection = self.graphicScene.items()[-1]
        dropRemoveSectionArea = dropRemoveSection.sceneBoundingRect()
        itemPosX = event.pos().x() 
        itemPosY = event.pos().y() + self.verticalScrollBar().sliderPosition()
        return (itemPosX >= (dropRemoveSectionArea.x() - dropRemoveSection.size)
            and itemPosX <= (dropRemoveSectionArea.topRight().x() + dropRemoveSection.size)
            and itemPosY >= (dropRemoveSectionArea.y() - dropRemoveSection.size)
            and itemPosY <= (dropRemoveSectionArea.bottomRight().y() + dropRemoveSection.size))
    
    def isItemInScene(self, item):
        return item in self.graphicScene.items()
    
    def displayDropRemoveArea(self, event:QDragMoveEvent):       
        dropRemoveSection = self.graphicScene.items()[-1]
        dropRemoveSection.setPos(self.width()/2 - 10,
                                    self.height() + self.verticalScrollBar().sliderPosition() - 100)
        if self.isInDropArea(event):
            dropRemoveSection.backGroundColor = QColor(Qt.GlobalColor.red)
            dropRemoveSection.borderColor = Qt.GlobalColor.red
            dropRemoveSection.update(dropRemoveSection.boundingRect())
        else:
            dropRemoveSection.backGroundColor = QColor(Qt.GlobalColor.gray)
            dropRemoveSection.borderColor = Qt.GlobalColor.darkGray
            dropRemoveSection.update(dropRemoveSection.boundingRect())   
    
        dropRemoveSection.show()

    def resetScene(self):
        while type(self.graphicScene.items()[0]) != XMarkItem:
            self.graphicScene.removeItem(self.graphicScene.items()[0])
        self.scene().setSceneRect(0, 0, 794, 1123) 

    def printToPdf(self):
        #paperHeight = self.sceneRect().height()

        options = QFileDialog.Option()
        #options |= QFileDialog.Option.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, 
            "Save PDF", "", "PDF(*.pdf)", options = options)
        
        if fileName != None: 
            printer = QPdfWriter(fileName)
            printer.setResolution(300)
            printer.setPageSize(QPageSize.PageSizeId.A4)
            printer.setTitle("Created by Ges Data Visualizer")
            printer.setCreator("GES VN")
            #printer.setResolution()
            painter = QPainter(printer)
            delta = 18*3.125
            f = painter.font()
            f.setPixelSize(delta)
            painter.setFont(f)

            self.graphicScene.clearFocus()
            tempScene = QGraphicsScene()
            tempScene.setSceneRect(0, 0, 2480, 3508 * self.pageCount)

            for item in self.graphicScene.items():
                if type(item) in [DraggableImageForPDF, Draggabletext]:
                    item.resizeToPrintResolution()
                    tempScene.addItem(item)

            highDpiPageHeight = self.pageHeight * 3.125
            pageRect = QRectF(0, 0, tempScene.sceneRect().width(), highDpiPageHeight)
            for page in range(self.pageCount):
                if page != 0:
                    printer.newPage()   
                tempScene.render(painter, QRectF(), pageRect)   
                #paperHeight -= self.pageHeight
                pageRect.translate(0, highDpiPageHeight)
            painter.end()

            for item in tempScene.items():
                if type(item) in [DraggableImageForPDF, Draggabletext]:
                    item.resizeToDisplayResolution()
                # elif type(item) is QGraphicsSimpleTextItem:
                #     item.setPos(self.pos().x() / 3.125, self.pos().y() / 3.125)

            for item in tempScene.items():
                self.graphicScene.addItem(item)

    def addNewPage(self):
        pageEndText = QGraphicsSimpleTextItem("---------------------------------End of page---------------------------------")
        pageEndText.setPos(self.sceneRect().width()/2 - pageEndText.boundingRect().width()/2,
                            self.pageCount * self.pageHeight - pageEndText.boundingRect().height())
        pageEndText.font().setPixelSize(15)
        pageEndText.setData(0, "page end text")
        self.graphicScene.addItem(pageEndText)
        newRect = QRectF(0, 0, self.sceneRect().width(), self.sceneRect().height() + self.pageHeight)
        self.scene().setSceneRect(newRect)
        self.pageCount += 1
        self.update()

    def itemMovedHandler(self, item):
        if item.sceneBoundingRect().bottomLeft().y() >= self.height() + self.verticalScrollBar().sliderPosition():
            QTimer.singleShot(200, lambda: self.verticalScrollBar().setSliderPosition(self.verticalScrollBar().sliderPosition() + 15))
        elif item.sceneBoundingRect().topLeft().y() <= self.verticalScrollBar().sliderPosition():
            QTimer.singleShot(200, lambda: self.verticalScrollBar().setSliderPosition(self.verticalScrollBar().sliderPosition() - 15))
    


