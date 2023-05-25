import sys
from PyQt5 import QtWidgets
from utils.snipping_tool import MyWidget

app = QtWidgets.QApplication(sys.argv)
window = MyWidget()

# window.show()
app.aboutToQuit.connect(app.deleteLater)
sys.exit(app.exec_())