from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import *
from utils.Constants import BASE_ANALYSIS_DIR
from PyQt5.QtGui import QPixmap
import os

class ImageWidget(QtWidgets.QWidget):
    def __init__(self,imgPath,tabWidget):
      super().__init__()
      uic.loadUi('ui/uifiles/final_result.ui',self)
      self.imgPath = imgPath
      self.tabWidget = tabWidget
      pixmap = QPixmap(imgPath)
    
     
    