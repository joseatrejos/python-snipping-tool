import sys, cv2, os
from PyQt5 import QtWidgets, QtCore, QtGui
from PIL import ImageGrab
import numpy as np
import tkinter as tk
import main as main

class MyWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super(MyWidget, self).__init__()
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.setGeometry(0, 0, screen_width, screen_height)
        self.setWindowTitle(' ')
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.parent = parent

    def start(self):
        self.setWindowOpacity(0.3)
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.CrossCursor)
        )
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor('black'), 3))
        qp.setBrush(QtGui.QColor(128, 128, 255, 128))
        qp.drawRect(QtCore.QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        QtWidgets.QApplication.restoreOverrideCursor()
        self.close()

        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())

        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))

        # Check if capture.png already exists. If it does, increment the filename by 1.
        i = 0
        while os.path.isfile(f'screenshots/capture{i}.png'):
            i += 1
        img.save(f'screenshots/capture{i}.png')
        image_path = f'screenshots/capture{i}.png'
        img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)

        window = main.MyMainWindow(image_path)


# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     window = MyWidget()
#     window.show()
#     app.aboutToQuit.connect(app.deleteLater)
#     sys.exit(app.exec_())
