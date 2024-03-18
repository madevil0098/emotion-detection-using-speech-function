from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QEvent,Qt
from code.db.Session import getAllSessions
from functools import partial
from ui.widget.SessionWidget import SessionWidget

class SessionRecordWidget(QtWidgets.QWidget):
    def __init__(self,mainWindow):
      super().__init__()
      self.index = 0
      self.mainWindow = mainWindow
      uic.loadUi('ui/uifiles/SessionRecords.ui',self)
      self.sessionWidget = None
      self.setupUI()
    def changeEvent(self, event):
      if event.type() == QEvent.WindowStateChange:
        if event.oldState()==Qt.WindowMinimized and (self.windowState() == Qt.WindowNoState or self.windowState() == Qt.WindowMaximized):
          if self.sessionWidget is not None:            
            self.sessionWidget.close()
    def setupUI(self):
      self.sessionTBL.setColumnCount(6)
      self.sessionTBL.setHorizontalHeaderLabels(["Session Title", "Date", "Start Time","Clustering","Analysis","View Details"])
      self.sessionTBL.setColumnWidth(0, 350)
      self.sessionTBL.setColumnWidth(1, 150)
      self.sessionTBL.setColumnWidth(2, 150)
      self.sessionTBL.setColumnWidth(3, 150)
      self.sessionTBL.setColumnWidth(4, 125)
      self.sessionTBL.setColumnWidth(5, 125)
      self.sessionTBL.setColumnWidth(6, 125)
      self.records = self.loadSessionRecords()
      self.setSessionRecords()
      self.nextBTN.clicked.connect(self.nextRecord)
      self.previousBTN.clicked.connect(self.preRecord)

    def nextRecord(self):
      #print("Next >> ")  
      self.index += 10
      self.records = self.loadSessionRecords()
      if len(self.records)==0:
        self.index -= 10
        self.records = self.loadSessionRecords()
      self.setSessionRecords()

    def preRecord(self):
      #print("Pre >> ")
      if self.index >0:
        self.index -= 10    
        self.records = self.loadSessionRecords()
        self.setSessionRecords()

    def loadSessionRecords(self):
      records = getAllSessions(self.index)            
      return records

    def viewSession(self,id):      
      sub = QMdiSubWindow()
      self.sessionWidget = sub
      sessWidget = SessionWidget(self.mainWindow,self,id)
      
      sub.setWidget(sessWidget)
      self.mainWindow.mdi.addSubWindow(sub)      
      center = self.mainWindow.mdi.viewport().rect().center()
      geo = sub.geometry()
      
      geo.moveCenter(center)
      sub.setGeometry(geo)
      sub.show()
      self.showMinimized()

    def setSessionRecords(self):
      self.sessionTBL.setRowCount(0)
      if self.records!=False:
        self.sessionTBL.setRowCount(len(self.records))
        for row in range(len(self.records)):
          rec = self.records[row]
          keys = list(rec.keys())
          #print("Keys : ",keys)
          viewBTN = QPushButton('View')
          viewBTN.resize(80,32)    
          for col in range(len(keys)):
            key = keys[col]
            #print("Key : ",key)
            if key=="session_id":              
              #print(rec[key])
              viewBTN.clicked.connect(partial(self.viewSession,rec[key]))
            elif key=="analysisDone":  
              analysisDone = ""
              if rec[key]==1:
                analysisDone = "Completed"
              else:
                analysisDone = "Pending"
              item = QTableWidgetItem(analysisDone)  
              self.sessionTBL.setItem(row,col-1,item)                
              self.sessionTBL.setCellWidget(row,col,viewBTN)        
            else:
              item = QTableWidgetItem(str(rec[key]))
              self.sessionTBL.setItem(row,col-1,item)
    def closeEvent(self,event):
        event.accept()
        self.mainWindow.menuSession.setEnabled(True)
    