from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from measure import processImage
from PIL import Image
from PIL.ImageQt import ImageQt 
import cv2

app = QApplication([])

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Fish Finder")
        self.resize(680,680)
        self.file_paths = []
        self.current_path = None
        self.output_image = None

        self.list_widget = selectionList(self)
        self.receiver_widget = receiver("Drop Images Here", self, self.list_widget)

    def setCurrentPath(self, child):
        if child.currentItem() is not None:
            self.current_path = child.currentItem().text()[8:]
            print("Set path to: " + child.currentItem().text()[8:])
            self.output_image = processImage(self.current_path, 1.905)
            #self.output_image = cv2.cvtColor(self.output_image, cv2.COLOR_BGR2RGB)
            #self.output_image = Image.fromarray(self.output_image).convert('RGB')
            #self.output_image = QPixmap.fromImage(ImageQt(self.output_image))

class selectionList(QListWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setGeometry(10,120,400,200)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.parent = parent
        self.currentItemChanged.connect(self.select)

    def select(self):
        self.parent.setCurrentPath(self)
        self.clearSelection()
        

#list_widget = QListWidget(self)
#list_widget.setGeometry(50,70,400,200)
#list_widget.setSelectionMode(QAbstractItemView.SingleSelection)

class receiver(QPushButton):
    def __init__(self, title, parent, listWidget):
        super().__init__(title, parent)
        self.setAcceptDrops(True)
        self.setGeometry(10,10,400,100)
        #self.current_path = None
        self.listWidget = listWidget

    def dragEnterEvent(self, e):

        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            for file in event.mimeData().text().split("\n"):
                print(file)
                self.listWidget.addItem(QListWidgetItem(file))

class ImageDisplay(QPixmap):
    
    pass

window = MainWindow()
window.show()
app.exec()