from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
import os
import time
import datetime
from code.db.Session import createSession
from utils.Constants import BASE_IMAGE_DIR
import shutil
import soundfile as sf



class VoiceClustor(QtWidgets.QWidget):
    def __init__(self,voice_Widgets):
        super().__init__() 
        self.Voice_Widgets = voice_Widgets
        
    
    def folder_sense(self,fname):
        voice_group=self.folder_voice(fname)
        print(voice_group)
        return self.folder_reconfig(voice_group)
        
        
    def folder_reconfig(self,fol:dict):
        count=0
        for i in fol:
            if fol[i] == None:
                continue
            if len(fol[i])!=0:
                if i=="wav" and fol[i]!=[]:
                    session_uuid = createSession("wav "+str(datetime.date.today()))
                    if session_uuid is not None:
                        folder = BASE_IMAGE_DIR + str(session_uuid)
                        os.makedirs(folder)
                        for j in fol["wav"]:
                            print(j)
                            if ".wav" in j[1]:
                                
                                shutil.copy(j[0], folder+"/"+j[1])   
                                count += 1 
                            else:    
                                data, samplerate = sf.read(j[0])
                                j=j[1].split(".")
                                sf.write(folder+"/"+j[0]+".wav", data, samplerate)          
                    else:  
                        QMessageBox.information(self, "Error","Somwthing Wrong to start Session !") 
                
                else:
                    session_uuid = createSession(i[-i[::-1].index("/"):])
                    if session_uuid is not None:
                        folder = BASE_IMAGE_DIR + str(session_uuid)
                        os.makedirs(folder)
                        
                        for j in fol[i]:
                            temp=self.folder_clear(fol[i][j])
                            for t in temp:
                                if ".wav" in j[1]:
                                    shutil.copy(t[0], folder+"/"+t[1])
                                    count +=1
                                else:    
                                    data, samplerate = sf.read(t[0])
                                    t=t[1].split(".")
                                    sf.write(folder+"/"+t[0]+".wav", data, samplerate)   
                    else:  
                        QMessageBox.information(self, "Error","Somwthing Wrong to start Session !")   
        return count
                    
        
    def folder_clear(self,element):
        if type(element)==list:
            return element
        else:
            temp=[]
            for i in element:
                if "wav" ==i:
                    temp.append(element[i])
                else:
                    temp.append(self.folder_clear(element[i]))
        return temp
        
    def folder_voice(self,fname):
        direct=os.listdir(fname)
        temp=dict()
        temp["wav"]=[]
        mon={"jan":1,"feb":2,"mar":3,"apr":4,"may":5,"jun":6,"jul":7,"aug":8,"sep":9,"oct":10,"nov":11,"dec":12}
        voice_extensions =["wav", "mp3", "m4a", "flac","mp4", "wma", "aac","opus"]
        #print(direct)
        for i in range(len(direct)):
            try:
                creation_time=os.path.getmtime(fname+"/"+direct[i])
                creation_time=str(time.ctime(creation_time)).split(" ")
                creation_time.remove("")
                today=str(datetime.datetime.now()).split(" ")
                creation_time[1]=mon[creation_time[1].lower()]
                today[0]=today[0].split("-")
                print(direct[i],creation_time)
                timedif=str(datetime.datetime.strptime(today[1].split(".")[0], "%H:%M:%S")-datetime.datetime.strptime(creation_time[3], "%H:%M:%S"))
                if int(creation_time[1])==int(today[0][1]) and int(creation_time[2])==int(today[0][2]) and creation_time[4]==today[0][0] and ("-" not in timedif):
                #if True:    
                    
                    timedif=timedif.split(":")
                    if int(timedif[1])<=300 and ("." not in direct[i]): 
                    #if ("." not in direct[i]): 
                        folderdict=self.folder_voice(fname+"/"+direct[i])
                        temp[fname+"/"+direct[i]]=folderdict
                    else:
                        direct[i]=direct[i].split(".")
                        print(direct[i],int(timedif[1])<=300,direct[i][-1].lower() in voice_extensions,int(timedif[1])<=300 and (direct[i][-1].lower() in voice_extensions))
                        if int(timedif[1])<=300 and (direct[i][-1].lower() in voice_extensions):
                            direct[i]=".".join(direct[i])
                            temp["wav"]=temp["wav"]+[(fname+"/"+direct[i],direct[i])]
            except Exception as e:
                print(e)
        return temp