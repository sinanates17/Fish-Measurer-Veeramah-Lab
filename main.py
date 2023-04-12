from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from measure import processImage
from PIL import Image
from PIL.ImageQt import ImageQt 
#import cv2
import os
from datetime import datetime
from time import sleep

app = QApplication([])

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Fish Finder")
        self.file_paths = []
        self.current_path = None
        self.output_image = None
        self.measurements = None
        self.known_width = 1.905
        self.resize(740,740)
        self.setFixedHeight(740)

        self.bold = QFont()
        self.bold.setBold(True)

        self.image_label = QLabel("Selected images will display here", self)
        self.image_label.move(520,10)
        self.image_label.adjustSize()

        self.measure_display = QTableWidget(self)
        self.measure_display.setGeometry(10,330,500,400)
        self.measure_display.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.list_widget = selectionList(self)
        self.receiver_widget = receiver("Drop Images Here", self, self.list_widget)

        self.known_width_input = QLineEdit(self)
        self.known_width_input.move(400,10)
        self.known_width_input.setFixedWidth(100)
        self.known_width_input.setStyleSheet("background-color: white;")
        self.known_width_input.setText("1.905")
        self.width_error = QLabel(self)
        self.width_error.move(220,23)
        self.width_error.setFixedWidth(180)
        self.width_error.setText("Must be a number!")
        self.width_error.setStyleSheet("QLabel { color : red }")
        self.width_error.setFont(QFont('Arial', 6))
        self.width_error.setFont(self.bold)
        self.width_error.hide()
        self.known_width_input.textChanged.connect(self.setKnownWidth)

        self.width_caption1 = QLabel(self)
        self.width_caption1.move(220,10)
        self.width_caption1.setFixedWidth(180)
        self.width_caption1.setText("Reference Width (cm):")
        self.width_caption1.setStyleSheet("QLabel { background-color : rgba(0,0,0,0) }")
        self.width_caption2 = QLabel(self)
        self.width_caption2.setGeometry(220,45,280,60)
        self.width_caption2.setWordWrap(True)
        self.width_caption2.setText("This is the known diameter of the reference object being used in cm.\nDefault: 1.095 (US penny)\nCurrent: " + str(self.known_width))
        self.width_caption2.setStyleSheet("QLabel { background-color : rgba(0,0,0,0); color : rgb(120,120,120) }")

        self.text_button1 = QPushButton(self)
        self.text_button2 = QPushButton(self)
        self.text_button1.setGeometry(220,230,140,60)
        self.text_button2.setGeometry(370,230,140,60)
        self.text_button1.setStyleSheet("background-color: rgb(220,220,230);")
        self.text_button2.setStyleSheet("background-color: rgb(220,220,230);")
        self.text_button1.setText("Selected image")
        self.text_button2.setText("All images")
        self.text_button1.clicked.connect(self.singleFiletxt)
        self.text_button2.clicked.connect(self.allFiletxt)
        
        self.txt_info = QLabel(self)
        self.txt_info.setGeometry(220,187,290,40)
        self.txt_info.setWordWrap(True)
        self.txt_info.setText("Generate a .txt file in /Outputs containing width/height data for:")
        self.txt_info.setStyleSheet("QLabel { background-color : rgba(0,0,0,0); color : rgb(120,120,120) }")

        self.txt_success = QLabel(self)
        self.txt_success.setGeometry(312,205,291,20)
        self.txt_success.setText("")
        self.txt_success.setFont(self.bold)
        self.txt_success.setStyleSheet("QLabel { background-color : rgba(0,0,0,0); color : green }")

        self.transpose_box = QCheckBox(self)
        self.transpose_box.setGeometry(220,290,290,40)
        self.transpose_box.setText("Transpose?")
      
        self.setStyleSheet("background-color: rgb(200,200,200);")

    def singleFiletxt(self):
        if self.current_path is None:
            self.txt_success.setText("Select an image!")
            self.txt_success.setStyleSheet("QLabel { background-color : rgba(0,0,0,0); color : red }")
            self.wait()
            self.txt_success.setText("")
            pass
        else:
            self.txt_success.setText("Working...")
            self.txt_success.setStyleSheet("QLabel { background-color : rgba(0,0,0,0); color : black }")
            dir = os.getcwd()+'/Output/'
            fname = self.current_path.split('/')[-1][:-4]+'.txt'
            with open(dir + fname,'w') as f:
                if self.transpose_box.isChecked():
                    f.write("Width:  ")
                    for point in self.measurements:
                        f.write(str(point[1])[0:4] + " ")
                    f.write("\nHeight: ")
                    for point in self.measurements:
                        f.write(str(point[2])[0:4] + " ")
                else:
                    f.write("Width , Height\n")
                    for point in self.measurements:
                        f.write(str(point[1])[0:4]+' '+str(point[2])[0:4]+'\n')
                f.write("\nCount: " + str(len(self.measurements)))
            self.txt_success.setText("Success!")
            self.txt_success.setStyleSheet("QLabel { background-color : rgba(0,0,0,0); color : green }")
            self.wait()
            self.txt_success.setText("")

    def allFiletxt(self):
        if not self.file_paths:
            self.txt_success.setText("Add files!")
            self.txt_success.setStyleSheet("QLabel { background-color : rgba(0,0,0,0); color : red }")
            self.wait()
            self.txt_success.setText("")
            pass
        else:
            self.txt_success.setText("Working...")
            self.txt_success.setStyleSheet("QLabel { background-color : rgba(0,0,0,0); color : black }")
            total_data = []
            dir = os.getcwd()+'/Output/'
            for item in self.file_paths:
                cvImage, data = processImage(item, self.known_width)
                for point in data:
                    total_data.append(point)
            time_now = datetime.now()
            fname = time_now.strftime("%m-%d-%y_%H-%M-%S")+".txt"
            with open(dir + fname,'w') as f:
                if self.transpose_box.isChecked():
                    f.write("Width:  ")
                    for point in total_data:
                        f.write(str(point[1])[0:4] + " ")
                    f.write("\nHeight: ")
                    for point in total_data:
                        f.write(str(point[2])[0:4] + " ")
                else:    
                    f.write("Width , Height\n")
                    for point in total_data:
                        f.write(str(point[1])[0:4]+' '+str(point[2])[0:4]+'\n')
                f.write("\nCount: " + str(len(total_data)))
            self.txt_success.setText("Success!")
            self.txt_success.setStyleSheet("QLabel { background-color : rgba(0,0,0,0); color : green }")
            self.wait()
            self.txt_success.setText("")

    def setCurrentPath(self, child):
        if child.currentItem() is not None:
            self.current_path = self.file_paths[child.currentRow()]
            #print("Set path to: " + child.currentItem().text()[8:])
    
    def setKnownWidth(self):
        try:
            self.known_width = float(self.known_width_input.text())
            self.width_caption2.setText("This is the known diameter of the reference object being used in cm.\nDefault: 1.095 (US penny)\nCurrent: " + str(self.known_width))
            self.width_error.hide()
        except:
            self.known_width = 1.905
            self.width_caption2.setText("This is the known diameter of the reference object being used in cm.\nDefault: 1.095 (US penny)\nCurrent: " + str(self.known_width))
            self.width_error.show()

    def wait(self):
        loop = QEventLoop()
        QTimer.singleShot(300, loop.quit)
        loop.exec_()

class selectionList(QListWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setGeometry(10,120,200,200)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.parent = parent
        self.currentItemChanged.connect(self.select)
        self.setStyleSheet("background-color: white;")

    def select(self):
        self.parent.setCurrentPath(self)
        cvImage, data = processImage(self.parent.current_path, self.parent.known_width)
        self.parent.measurements = data
        height, width, channel = cvImage.shape
        bytesPerLine = 3 * width

        self.parent.current_image = QPixmap.fromImage(QImage(cvImage.data, width, height, bytesPerLine, QImage.Format_BGR888))
        self.parent.image_label.setPixmap(self.parent.current_image)
        self.parent.image_label.adjustSize()

        self.parent.measure_display.setRowCount(len(data)+1)
        self.parent.measure_display.setColumnCount(3)
        self.parent.measure_display.setHorizontalHeaderLabels(['Fish', 'Width (cm)', "Height (cm)"])
        headers = self.parent.measure_display.horizontalHeader()
        headers.setSectionResizeMode(0, 50)
        headers.setSectionResizeMode(1, QHeaderView.Stretch)
        headers.setSectionResizeMode(2, QHeaderView.Stretch)

        for point in data:
            if point[0] == "":
                continue
            self.parent.measure_display.setItem(point[0]-1,0,QTableWidgetItem(str(point[0])))
            self.parent.measure_display.setItem(point[0]-1,1,QTableWidgetItem(str(point[1])[0:4]))
            self.parent.measure_display.setItem(point[0]-1,2,QTableWidgetItem(str(point[2])[0:4]))
        self.parent.resize(520 + width, 740)

class receiver(QPushButton):
    def __init__(self, title, parent, listWidget):
        super().__init__(title, parent)
        self.setAcceptDrops(True)
        self.setGeometry(10,10,200,100)
        self.setAutoFillBackground(True)
        self.listWidget = listWidget
        self.parent = parent
        self.setStyleSheet("background-color: rgb(220,220,230);")

    def dragEnterEvent(self, e):

        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            for file in event.mimeData().text().split("\n"):
                if file == "":
                    continue
                #print(file)
                self.parent.file_paths.append(file[8:])
                self.listWidget.addItem(QListWidgetItem(file.split("/")[-1]))

window = MainWindow()
window.show()
app.exec()