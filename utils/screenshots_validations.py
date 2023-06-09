from PyQt5.QtWidgets import QMessageBox
import os

def validate_folder(window, path):
    if os.path.exists(path):
        screenshots = os.listdir(path)
        
        if screenshots:
            return path
        else:
            message = "The are no files in the folder."
            QMessageBox.information(window, "Info", message, QMessageBox.Ok)
    else:
        create_folder(window, path)
        message = "The folder didn't exist. \nIt has been created."
        QMessageBox.warning(window, "Alert", message, QMessageBox.Ok)

def create_folder(window, path):
    try:
        os.mkdir(path)
    except OSError:
        message = "nCould not create the folder."
        QMessageBox.warning(window, "Alert", message, QMessageBox.Ok)

def exist_folder(window, path):
    if os.path.exists(path):
        screenshots = os.listdir(path)

        if screenshots:
            return True
        else:
            return False
    else:
        create_folder(window, path)

