from PyQt5.QtWidgets import *

from ui.widget.VoiceRecog import VoiceRecogWidget
from ui.widget.SessionRecordWidget import SessionRecordWidget   


class MyAction:
    def __init__(self,mainWindow):
        self.mainWindow = mainWindow

    def voiceRecords(self):
        sub = QMdiSubWindow()
        sub.setWidget(VoiceRecogWidget(self.mainWindow))
        sub.setWindowTitle("Voice Recognition")
        self.mainWindow.mdi.addSubWindow(sub)
        sub.show()
        center = self.mainWindow.mdi.viewport().rect().center()
        geo = sub.geometry()
        geo.moveCenter(center)
        sub.setGeometry(geo)
        self.mainWindow.menuSession.setEnabled(False)
        
    def sessionRecords(self): 
        sub = QMdiSubWindow()
        sub.setWidget(SessionRecordWidget(self.mainWindow))
        self.mainWindow.mdi.addSubWindow(sub)
        sub.show()
        center = self.mainWindow.mdi.viewport().rect().center()
        geo = sub.geometry()
        geo.moveCenter(center)
        sub.setGeometry(geo)
        self.mainWindow.menuSession.setEnabled(False)
        
    def file_change(self):
        fname = QFileDialog.getExistingDirectory(self.mainWindow, 'Open folder')
        ffolder=open("foldersave.txt", "w")
        ffolder.write(fname)
        ffolder.close()