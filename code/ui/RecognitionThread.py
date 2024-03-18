import os
from PyQt5.QtWidgets import *
from code.ui.VoiceThread import VoiceThread
from pydub.audio_segment import AudioSegment
from utils.Constants import BASE_ANALYSIS_DIR
from code.db.Session import recognitionDoneSession
from PyQt5 import QtCore

class RecognitionThread(QtCore.QThread):
    signal = QtCore.pyqtSignal(int)

    
    def __init__(self,sessionWidget):
        super().__init__(parent=sessionWidget)
        
        self.sessionWidget = sessionWidget
        self.sessionId = sessionWidget.sessionId
        self.noOfCluster = sessionWidget.session.get('noOfCluster')
        self.baseDir = BASE_ANALYSIS_DIR+"/"+self.sessionId
        if not os.path.exists(self.baseDir):
            QMessageBox.information(self.sessionWidget, "Information",
                                        "Capture Images Folder Not Found !")
            
            sessionWidget.msgLBL.setText("Capture Images Folder Not Found !")
    def run(self):
        self.sessionWidget.msgLBL.setText("Recognition is Starting ...... ")
        dirs = os.listdir(self.baseDir)
        emotions=['neutral','calm','happy','sad','angry','fearful','disgust','surprised']
        for i in range(self.noOfCluster):
            folder = self.baseDir+"/label"+str(i)
            folderContents = os.listdir(folder)
            name=folder+"/group.csv"
            f=open(name,'w',newline='')
            f.close()
            for filename in folderContents:
                if filename.startswith("lbl_") or "wav" not in filename:
                    continue
                file = folder+"/"+filename
                #self model
                print(file)
                
                song=AudioSegment.from_wav(file)

                slash=10000
                
                slise=[]
                print(len(song))
                for slash2 in range(0,len(song),10000):
                    
                    slise.append(song[slash2:slash])
                    slash=slash+10000
                if os.path.exists(folder+"/chuncks") == False:
                    os.makedirs(folder+"/chuncks")
                #print(slise)
                for i in range(0,len(slise)):
                    slise[i].export(folder+"/chuncks/chunk{0}.wav".format(i), bitrate ='192k', format ="wav")
                for i in range(0,len(slise)):
                    self.analysisOb = VoiceThread(self.sessionWidget,False,folder+"/chuncks/chunk{0}.wav".format(i),folder+"/group.csv")
                    print('Voice Start ..... ') 
                    self.analysisOb.start()
                    
                    
        recognitionDoneSession(self.sessionId)
        self.sessionWidget.msgLBL.setText("Recognition is Complete ...... ")
        self.signal.emit(self.noOfCluster)
        
       