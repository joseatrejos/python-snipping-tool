from PyQt5.QtWidgets import QMessageBox
import os

def validate_script(window, file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()

            if content:
                return file_path
            else:
                message = "There are no instructions in the script yet"
                QMessageBox.information(window, "Info", message, QMessageBox.Ok)

    except FileNotFoundError:
        message = "No automated process script found. \nDon't worry it will be created."
        QMessageBox.warning(window, "Alert", message, QMessageBox.Ok)
        create_script(window, file_path)

def create_script(window, file_path):
    try:
        open(file_path, 'w')
    except IOError:
        message = "Could not create script."
        QMessageBox.warning(window, "Alert", message, QMessageBox.Ok)


def exist_script(window, file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            content = file.read()
            if content:
                return True
            else:
                return False
    else:
        create_script(window, file_path)