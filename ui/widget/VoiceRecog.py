from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import *
from code.ui.VoiceThread import VoiceThread
from ui.widget.VoiceCluster import VoiceClustor
import soundfile as sf


class VoiceRecogWidget(QtWidgets.QWidget):
    def __init__(self,mainWindow):
      super().__init__()      
      self.mainWindow = mainWindow
      self.VoiceClustor=VoiceClustor(self)
      uic.loadUi('ui/uifiles/VoiceRecog.ui',self)
      self.startbtn.clicked.connect(self.start)
      self.uploadbtn.clicked.connect(self.upload)

    def start(self):
      
      ffolder=open("foldersave.txt", "a+")
      ffolder.seek(0)
      fname=ffolder.read()
      if fname=="" :
        fname=QFileDialog.getExistingDirectory(self, 'Open folder')
        ffolder.write(fname)
      
      t=self.VoiceClustor.folder_sense(fname)
      self.msglbl.setText("Message : ")
      self.remlbl.setText("Done "+str(t)+" elements added") 
      ffolder.close()
      
      
      """
      self.folder_voice()
      self.analysisOb = VoiceThread(self,True,None)
      print('Voice Start ..... ') 
      self.msglbl.setText("Message : ")
      self.remlbl.setText("Recording Running for 4 Seconds ....")  
      self.analysisOb.start()"""
    def upload(self):
      fname = QFileDialog.getOpenFileName(self, 'Open file')
      path = fname[0]
      if '.wav' not in path:
        data, samplerate = sf.read(path)
        sf.write(".\\test\\file.wav", data, samplerate)
        
        
        path=".\\test\\file.wav"
      self.analysisOb = VoiceThread(self,False,path,".\\test\\group.csv")
      print('Voice Start ..... ') 
      self.msglbl.setText("Message : ")
      self.remlbl.setText("Analysis File ...... ")  
      self.analysisOb.start()
    
    
    