import math
import sys
from PyQt5.QtWidgets import QAction, QApplication, QMainWindow, QPushButton, QWidget, QMenu, QHBoxLayout, QVBoxLayout, QLabel, QMessageBox
from PyQt5.QtGui import QPalette, QColor, QPixmap, QFont, QImage
from PyQt5.QtCore import Qt
import os
import subprocess
import keyboard
import threading
from image_recognition import run_script

from utils.script_validations import validate_script, exist_script
from utils.screenshots_validations import validate_folder, exist_folder
import snipping_tool as SnippingTool

class MyMainWindow(QMainWindow):
    default_title = "Process automation"

    def __init__(self, image_path=None):
        super().__init__()

        self.image_path = image_path
        self.title = MyMainWindow.default_title
        self.setGeometry(200, 200, 500, 300)
        keyboard.on_press_key('q', self.stop_process)

        # Crear acciones de menús
        edit_process = QAction('Edit process', self)
        edit_process.triggered.connect(self.edit_process_clicked)

        erase_process = QAction('Erase process', self)
        erase_process.triggered.connect(self.erase_process_clicked)

        open_folder = QAction('Open folder', self)
        open_folder.triggered.connect(self.open_folder_clicked)

        erase_images = QAction('Erase images', self)
        erase_images.triggered.connect(self.erase_images_clicked)

        # Crear menús
        process_menu = QMenu('Process', self)
        process_menu.addAction(edit_process)
        process_menu.addAction(erase_process)

        images_menu = QMenu('Images', self)
        images_menu.addAction(open_folder)
        images_menu.addAction(erase_images)

        # Agregar el menú a la barra de menú
        menu_bar = self.menuBar()
        menu_bar.addMenu(process_menu)
        menu_bar.addMenu(images_menu)
        menu_bar.addAction("Exit", self.close)

        center_widget = QWidget(self)
        self.setCentralWidget(center_widget)
        main_layout = QVBoxLayout(center_widget)

        self.section1 = QVBoxLayout()
        self.image_label = QLabel()
        
        if image_path is not None:
            self.image = QPixmap(image_path)
        else:
            self.image = QPixmap("media/automatizacion.png") 
        self.image_label.setPixmap(self.image)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.section1.addWidget(self.image_label)

        # Crear la segunda sección vertical
        section2 = QHBoxLayout()

        # Crear los buttones
        button1 = QPushButton("Initialize process")
        button1.clicked.connect(self.initialize_process_clicked)
        button1.setFixedHeight(30)
        button1.setFont(QFont("MS Shell Dlg", 10))
        section2.addWidget(button1)

        button2 = QPushButton("Automate new step")
        button2.clicked.connect(self.automate_new_process_clicked)
        button2.setFixedHeight(30)
        button2.setFont(QFont("MS Shell Dlg", 10))
        section2.addWidget(button2)

        # Agregar las secciones al layout principal
        main_layout.addLayout(self.section1)
        main_layout.addLayout(section2)
          
        self.snipping_tool = SnippingTool.MyWidget(self)
        self.initialize = False
        self.show()

    def initialize_process_clicked(self):
        exist_folder(self, 'scripts')
        file_path = exist_script(self, 'scripts/script.txt')
        folder_path = exist_folder(self, 'screenshots')
        
        if file_path and folder_path:
            if not self.initialize:
                self.initialize = True
                QMessageBox.information(self, "How to", "This window will hide and start an infinite loop executing the defined script, to stop it press \"Ctrl+Q\"")
                self.hide()    
                self.loop_thread = threading.Thread(target=self.infinite_loop)
                self.loop_thread.start()
        else:
            message = "No automated process script or images found. \nCreate a new automated step"
            QMessageBox.warning(window, "Alert", message, QMessageBox.Ok)

            
    def infinite_loop(self):
        while self.initialize:
            file = open('scripts/script.txt', 'r')
            script = file.read()
            run_script(script)
        self.show()

    def stop_process(self, event):
        if event.event_type == 'down' and event.name == "q" and keyboard.is_pressed('ctrl'):
            self.initialize = False
            print("Closing...")
               

    def automate_new_process_clicked(self):
        exist_folder(self, 'scripts')
        file_path = exist_script(self, 'scripts/script.txt')
        folder_path = exist_folder(self, 'screenshots')
        
        if not file_path and not folder_path:
            QMessageBox.information(self, "How to", "Now you will take a screenshot of what you want, which will be displayed on the current screen of this software, where you must click on what you want to repeat and it will be saved automatically")

        self.close()
        self.snipping_tool.start()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            x = event.x()
            y = event.y()

            label_width = self.image_label.width()
            label_height = self.image_label.height()

            label_pos = self.image_label.pos()
            x_label = label_pos.x()
            y_label = label_pos.y()

            pixmap = self.image_label.pixmap()
            img_width = pixmap.width()
            img_heigth = pixmap.height()

            if x >= (label_width - img_width)/2 + x_label and x <= (label_width - img_width)/2 + img_width + x_label and y >= (label_height - img_heigth)/2 + y_label + 20 and y <= (label_height - img_heigth)/2 + img_heigth + y_label + 20:
                if self.image_path is not None:
                    x = math.floor(x - ((label_width - img_width)/2 + x_label))
                    y = math.floor(y - ((label_height - img_heigth)/2 + y_label + 20))

                    with open('scripts/script.txt', 'a') as file:
                        file.write(f'{self.image_path}|{x}|{y}\n')

                    message = "Automated step saved successfully"
                    QMessageBox.information(self, "Alert", message)
                    self.clean_interface()
                    
    def clean_interface(self):
        self.close()
        MyMainWindow()
        
    def edit_process_clicked(self):
        exist_folder(self, 'scripts')
        file_path = validate_script(self, 'scripts/script.txt')
        if file_path:
            try:
                subprocess.run(['start', '', file_path], shell=True)
            except subprocess.CalledProcessError:
                message = "Could not open script."
                QMessageBox.warning(self, "Alert", message, QMessageBox.Ok)

    def erase_process_clicked(self):
        exist_folder(self, 'scripts')
        file_path = validate_script(self, 'scripts/script.txt')
        if file_path:
            try:
                os.remove(file_path)
            except PermissionError:
                message = "You don't have the permission to delete the script."
                QMessageBox.warning(self, "Alert", message, QMessageBox.Ok)
            except OSError:
                message = "Error deleting script."
                QMessageBox.warning(self, "Alert", message, QMessageBox.Ok)

    def open_folder_clicked(self):
        folder = validate_folder(self, 'screenshots')
        if folder:
            try:
                subprocess.run(['explorer', folder])
            except subprocess.CalledProcessError:
                message = "Could not open the folder."
                QMessageBox.warning(self, "Alert", message, QMessageBox.Ok)

    def erase_images_clicked(self):
        folder = validate_folder(self, 'screenshots')
        if folder:
            try:
                images = os.listdir(folder)

                for image in images:
                    image_path = os.path.join(folder, image)
                    if os.path.isfile(image_path):
                        os.remove(image_path)
                
            except NotADirectoryError():
                message = "The path does not correspond to a valid folder."
                QMessageBox.warning(self, "Alert", message, QMessageBox.Ok)
            except PermissionError():
                message = "You don't have the permission to delete the script."
                QMessageBox.warning(self, "Alert", message, QMessageBox.Ok)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Establecer el estilo oscuro
    app.setStyle("Fusion")
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Text, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
    app.setPalette(dark_palette)

    # Crear una instancia de MyMainWindow
    window = MyMainWindow()

    # Iniciar el bucle de eventos
    sys.exit(app.exec())
