from PyQt5 import QtCore
import sounddevice as sd
from scipy.io.wavfile import write
import librosa            #to feature extraction
import os                 #to obtain the file
import glob               #to obtain filename having the same pattern
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
import soundfile
import pandas as pd
import csv

class VoiceThread(QtCore.QThread):
    def __init__(self,recognition,isRecord,fpath,data_path):
        super().__init__(recognition)
        
        self.duration = 10
        self.isRecord = isRecord
        self.fpath = fpath
        self.data_path=data_path
        #DataFlair - Emotions in the RAVDESS dataset
        self.emotions={
        '01':'neutral',
        '02':'calm',
        '03':'happy',
        '04':'sad',
        '05':'angry',
        '06':'fearful',
        '07':'disgust',
        '08':'surprised'
        }
        #DataFlair - Emotions to observe
        self.observed_emotions=['calm', 'happy', 'fearful', 'disgust']

    def extract_feature(self,file_name, mfcc, chroma, mel):
        with soundfile.SoundFile(file_name) as sound_file:
            X = sound_file.read(dtype="float32")
            X = X.flatten()
            sample_rate=sound_file.samplerate
            if chroma:
                stft=np.abs(librosa.stft(X))
            result=np.array([])
            if mfcc:
                mfccs=np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
                result=np.hstack((result, mfccs))
            if chroma:
                chroma=np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)
                result=np.hstack((result, chroma))
            if mel:
                mel=np.mean(librosa.feature.melspectrogram(y=X, sr=sample_rate).T,axis=0)
                result=np.hstack((result, mel))
            return result

    #DataFlair - Load the data and extract features for each sound file
    def load_data(self,test_size=0.2):
        x,y=[],[]
        for file in glob.glob("static/dataset/Actor_*/*.wav"):
            
            file_name=os.path.basename(file)
            emotion=self.emotions[file_name.split("-")[2]]
            if emotion not in self.observed_emotions:
                continue
            feature=self.extract_feature(file, mfcc=True, chroma=True, mel=True)
            x.append(feature)
            y.append(emotion)
            print(file,feature.shape)
        return train_test_split(np.array(x), y, test_size=test_size, random_state=9)
        
    
    def run(self):
        if(self.isRecord):
            # Sampling frequency
            #freq = 44100
            freq = 44100   
            # Recording duration
            duration = 4
    
            # Start recorder with the given values 
            # of duration and sample frequency
            recording = sd.rec(int(duration * freq), 
                    samplerate=freq, channels=2)  
            sd.wait()             
            write("recording0.wav", freq, recording)        
        
        #DataFlair - Split the dataset
        #x_train,x_test,y_train,y_test=self.load_data(test_size=0.25)

        ddf = pd.read_csv('static/voice.csv')
        ddf_features = ddf.iloc[:,0:180]
        ddf_lbls = ddf.iloc[:,180]
        # print(ddf_features.shape)
        # print(ddf_lbls.shape)
        # print(ddf_features)
        # print(ddf_lbls)
        
        x_train,x_test,y_train,y_test=train_test_split(ddf_features, ddf_lbls, test_size=0.25, random_state=9)

        #DataFlair - Initialize the Multi Layer Perceptron Classifier
        model = MLPClassifier(alpha=0.01, batch_size=256, epsilon=1e-08, hidden_layer_sizes=(300,), learning_rate='adaptive', max_iter=500)
        #DataFlair - Train the model
        model.fit(x_train,y_train)
        #DataFlair - Predict for the test set
        if self.isRecord:
            feature= self.extract_feature("recording0.wav", mfcc=True, chroma=True, mel=True)
        else:
            feature= self.extract_feature(self.fpath, mfcc=True, chroma=True, mel=True)    
        y_pred=model.predict(feature.reshape(1, -1))
        print(y_pred)
        file=open(self.data_path,"a+",newline="")
        fol=csv.writer(file)
        fol.writerow([self.fpath,y_pred[0]])
        file.close()
       
        """self.voiceWidget.remlbl.setText("Done .....")
        self.voiceWidget.msglbl.setText("Message : " + y_pred[0])"""
