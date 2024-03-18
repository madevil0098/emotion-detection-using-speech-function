from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from code.db.Session import getSession
from code.ui.ClusterThread import ClusterThread
from code.ui.RecognitionThread import RecognitionThread
from ui.widget.ClusterTabWidget import ClusterTabWidget


class SessionWidget(QtWidgets.QWidget):
    def __init__(self,mainWindow,sessionRecordWidget,sessionId):
      super().__init__()
      self.sessionRecordWidget = sessionRecordWidget
      self.mainWindow = mainWindow
      uic.loadUi('ui/uifiles/SessionDetail.ui',self)
      self.sessionId = sessionId
      self.session = getSession(sessionId)
      if self.session==False:
        QMessageBox.information(self, "Information",
                                        "Invalid Session !") 
        self.close()  
      else:
        self.setupUI()
    def recognize(self):
      self.recogOb = RecognitionThread(self)   
      self.recogOb.signal.connect(self.showCluster)
      self.recogOb.start()
      self.recogBTN.setEnabled(False)

    def analysis(self):
      
      self.analysisOb = ClusterThread(self)
      self.analysisOb.signal.connect(self.showCluster)
      
      print('Analysis Start ..... ')    
      self.analysisOb.start()

    def showCluster(self,uniqueFaceCount):
      print(uniqueFaceCount)
      self.session = getSession(self.sessionId)
      self.refreshBTN()
      self.tabWidget.clear()  
      for i in range(uniqueFaceCount):
         tab = ClusterTabWidget(self.sessionId,i)
         self.tabWidget.addTab(tab, "customer "+str(i+1))    

    def setupUI(self):
      self.tabWidget.clear()  
      self.titleLBL.setText(self.session.get('session_title'))
      self.dateLBL.setText("Date : " + str(self.session.get('session_date')))
      self.startTimeLBL.setText("Start Time : " + str(self.session.get('session_start_time')))
      if self.session.get('clusteringDone'):
        self.showCluster(self.session.get('noOfCluster'))
      else:
        self.tabWidget.setEnabled(False)
        self.recogBTN.setEnabled(False)
        self.analysisBTN.clicked.connect(self.analysis)  

    def refreshBTN(self):
      if self.session.get('clusteringDone'):
        self.analysisBTN.setEnabled(False)
        self.tabWidget.setEnabled(True)        
        if self.session.get('analysisDone'):
           self.recogBTN.setEnabled(False)
        else:
           self.recogBTN.setEnabled(True)   
           self.recogBTN.clicked.connect(self.recognize)
      else:
        self.tabWidget.setEnabled(False)
        self.recogBTN.setEnabled(False)
        #self.analysisBTN.clicked.connect(self.analysis)
    def closeEvent(self,event):      
      print("Closing")
      self.sessionRecordWidget.sessionWidget=None