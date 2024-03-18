from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from code.db.Session import createSession

class NewSessionWidget(QtWidgets.QWidget):
    def __init__(self,mainWindow):
      super().__init__()
      self.mainWindow = mainWindow
      uic.loadUi('ui/uifiles/NewSession.ui',self)

      self.pauseBTN.setEnabled(False)
      self.stopBTN.setEnabled(False)

      self.setupEvents()

    def setupEvents(self):
      self.startBTN.clicked.connect(self.startSession)
      self.stopBTN.clicked.connect(self.stopSession)

    def startSession(self):
      title = self.titleTXT.text()
      if len(title)>0:
        self.pauseBTN.setEnabled(True)
        self.stopBTN.setEnabled(True)
        self.startBTN.setEnabled(False)
        session_uuid = createSession(self.titleTXT.text())
        
        if session_uuid is not None:
          self.mainWindow.startSession(self,session_uuid)
        else:  
          QMessageBox.information(self, "Error",
                                        "Somwthing Wrong to start Session !")  
      else:      
        QMessageBox.information(self, "Error",
                                        "Title Can Not be Empty !")  
    def stopSession(self):
      self.pauseBTN.setEnabled(False)
      self.stopBTN.setEnabled(False)
      self.startBTN.setEnabled(True)
      self.mainWindow.stopSession(self)  

    def closeEvent(self,event):
      if self.mainWindow.isSessionRunning:
        QMessageBox.information(self, "Information",
                                        "Session is running !")
        event.ignore()
      else:
        buttonReply = QMessageBox.question(self, 
        'Closing Message', "Are You Sure To Exit ?",
         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
         
        if buttonReply == QMessageBox.Yes:            
           event.accept()
           self.mainWindow.menuSession.setEnabled(True)
        else:
          event.ignore()
      
      
   
