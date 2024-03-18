import os
import shutil
from PyQt5.QtWidgets import *
from utils.Constants import BASE_IMAGE_DIR,BASE_ANALYSIS_DIR
from code.db.Session import analysisDoneSession

from PyQt5 import QtCore

class ClusterThread(QtCore.QThread):
    signal = QtCore.pyqtSignal(int)
    def __init__(self,sessionWidget):
        super().__init__(parent=sessionWidget)
        
        self.sessionWidget = sessionWidget
        self.session_uuid = sessionWidget.sessionId
        self.baseDir = BASE_IMAGE_DIR+"/"+self.session_uuid
        if not os.path.exists(self.baseDir):
            QMessageBox.information(self, "Information",
                                        "Capture Images Folder Not Found !")
            sessionWidget.msgLBL.setText("Capture Images Folder Not Found !")
    def move_image(self,image,id,labelID):	
        folder = BASE_ANALYSIS_DIR+self.session_uuid  
        path = folder +'/label'+str(labelID)
        if os.path.exists(path) == False:
            os.mkdir(path)
        filename = str(id) 
        shutil.copy(self.baseDir+"/"+image, os.path.join(path , filename))
        

    def run(self):
        self.sessionWidget.msgLBL.setText("Encoding is Starting ...... ")
        imagePaths = os.listdir(self.baseDir)
        print(imagePaths)
        folder = BASE_ANALYSIS_DIR+self.session_uuid    
        if not os.path.exists(folder):
            os.makedirs(folder)    
        self.sessionWidget.msgLBL.setText("Clustering is Start ...... ")
        numUniqueFaces = len(imagePaths)
        print("Num of faces : ",numUniqueFaces)
        
        for i in range(numUniqueFaces):
            self.move_image(imagePaths[i],imagePaths[i],i)
            
        self.sessionWidget.msgLBL.setText("Clustering is Completed ...... ")    
        self.sessionWidget.analysisBTN.setEnabled(False)
        self.sessionWidget.tabWidget.setEnabled(True)
        analysisDoneSession(self.session_uuid,numUniqueFaces)
        #self.sessionWidget.showCluster(numUniqueFaces)
        self.sessionWidget.session['clusteringDone'] = True
        self.signal.emit(numUniqueFaces)