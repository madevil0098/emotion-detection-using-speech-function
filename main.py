import sys
from PyQt5 import QtWidgets
from ui.frame.MainWindow import MainWindow
app = QtWidgets.QApplication(sys.argv)
ui = MainWindow()
ui.show()
sys.exit(app.exec_())