from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap

class ImageWidget(QtWidgets.QWidget):
    def __init__(self,imgPath,tabWidget):
      super().__init__()
      uic.loadUi('ui/uifiles/Image.ui',self)
      self.imgPath = imgPath
      self.tabWidget = tabWidget
      pixmap = QPixmap(imgPath)
      self.imgLBL.setPixmap(pixmap)
      