from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import *
from utils.Constants import BASE_ANALYSIS_DIR
from os import listdir
from os.path import isfile, join
from code.db.Session import getSession
from ui.widget.voiceWidget import voiceWidget
from ui.widget.ImageWidget import ImageWidget
import matplotlib.pyplot as plt
import pandas
from PyQt5 import QtCore

class ClusterTabWidget(QtWidgets.QWidget):
    signal = QtCore.pyqtSignal(int)
    def __init__(self,sessionId,index):
      super().__init__()
      self.sessionId = sessionId
      self.session = getSession(sessionId)
      self.index = index
      uic.loadUi('ui/uifiles/ClusterTab.ui',self)
      self.layout = QtWidgets.QHBoxLayout(self)
      self.scrollArea = QtWidgets.QScrollArea(self)
      self.scrollArea.setWidgetResizable(True)
      self.gridLayout = QtWidgets.QGridLayout(self.frame)
      self.scrollArea.setWidget(self.frame)
      self.layout.addWidget(self.scrollArea)
      self.showAllImages()

    def clearGrid(self):
      for i in reversed(range(self.gridLayout.count())): 
        self.gridLayout.itemAt(i).widget().setParent(None)
    def showAllImages(self):
      
      
      self.clearGrid()
      folder = BASE_ANALYSIS_DIR + self.sessionId + "/label" + str(self.index)
      #print(folder) 
      try:
        
        emotions=['neutral','calm','happy','sad','angry','fearful','disgust','surprised']
        lables=pandas.read_csv(folder+"/group.csv",header=None)
        
        data=dict()
 
        for j in emotions:  
            data[j]=list(lables[lables.columns[1]]).count(j)
        
        courses = list(data.keys())
        values = list(data.values())
        my_dpi=96
        plt.figure(figsize=(620/my_dpi, 220/my_dpi), dpi=my_dpi)
        # creating the bar plot
        plt.bar(courses, values,color="green")
        file = folder+"/lbl_img.jpg"
        plt.savefig(file)
      except Exception as e:
        print(e)
       
      row=0
      col=0
      for content in reversed(listdir(folder)):       
        if isfile(join(folder, content)):                  
          if not self.session.get('analysisDone') and content.startswith("lbl_"):  
              continue   
          if "wav" in content:
            self.gridLayout.addWidget(voiceWidget(join(folder, content),self),row,col)
          if content.startswith("lbl_") and (("jpg" in content) or ("jpeg" in content)):  
            self.gridLayout.addWidget(ImageWidget(join(folder, content),self),row,col)
          
            
            
            
          