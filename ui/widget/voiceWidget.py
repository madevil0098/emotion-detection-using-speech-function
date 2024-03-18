from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

class voiceWidget(QtWidgets.QWidget):
    def __init__(self,imgPath,tabWidget):
      super().__init__()
      uic.loadUi('ui/uifiles/form.ui',self)
      self.imgPath = imgPath
      self.tabWidget = tabWidget
      self.mode=False
      self.player = QMediaPlayer()
      self.icon="ui/uifiles/play.jpeg"
      self.song=self.player.duration
      self.increase_progress=0
      self.pushButton.setIcon(QIcon(self.icon))
      self.progressBar.setValue(0)
      self.pushButton.clicked.connect(self.play)
      self.player.positionChanged.connect(self.positionChanged)
      self.player.durationChanged.connect(self.durationChanged)
    
      
      
    def positionChanged(self, position):
        self.progressBar.setValue(position)

    def durationChanged(self, duration):
        self.progressBar.setRange(0, duration)
        
    def play(self):
      self.mode=True
      self.icon="ui/uifiles/pause.jpeg"
      self.pushButton.setIcon(QIcon(self.icon))
    
      
      self.pushButton.clicked.connect(self.pause)
      self.pushButton.clicked.disconnect(self.play)
      url = QUrl.fromLocalFile(self.imgPath)
      content = QMediaContent(url)

      self.player.setMedia(content)
      self.player.play()
    def pause(self):
      self.mode=False
      self.icon="ui/uifiles/play.jpeg"
      self.pushButton.setIcon(QIcon(self.icon))
      self.player.pause()
    
      self.pushButton.clicked.connect(self.play)
      self.pushButton.clicked.disconnect(self.pause)
      
