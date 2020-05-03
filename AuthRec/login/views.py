# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

from .Backend import GMMTesting
from .Backend import GMMTraining
from .Backend import preprocessing
from .Backend import recognition

import sounddevice
from scipy.io.wavfile import write
import subprocess
from subprocess import getoutput as gt


def recording(Name, Range, Path, second) :
    sr =44100
    if Range == 10 :
        record_voice=sounddevice.rec(int(second * sr),samplerate=sr,channels=2)
        sounddevice.wait()
        fname=Name
        write(fname,sr,record_voice)
        return
    
    for i in range(Range) : 
        record_voice=sounddevice.rec(int(second * sr),samplerate=sr,channels=2)
        sounddevice.wait()
        fname=Name+str(i+1)+".wav"
        write(fname,sr,record_voice)

# Create your views here.
def home(request):
    return render(request,'home.html')

def main(request):
    val = int(request.POST['input'])
    if (val == 1):
        return render(request,'login.html')
    else:
        return render(request,'register.html')

def register(request):
    name = request.POST['name']
    record = request.POST['record']
    passRecord = request.POST['pass']
    if (name and record and passRecord):
        passpath = "login/Backend/PasswordData/"+name
        # gt("mkdir %s" %(passpath))
        proc=subprocess.Popen("mkdir "+passpath, shell=True)
        proc.wait()        
        recording(name,1,passpath, 8)
        # gt("mv %s %s" %(name+"1.wav" , passpath)) 
        subprocess.call(["mv", name+"1.wav", passpath])
        return render(request, 'home.html')
    if (name and record):
        path = "login/Backend/TrainingData/" + name
        proc=subprocess.Popen("mkdir "+path, shell=True)
        proc.wait()
        recording(name , 5 , path, 6)
        for i in range(5) :
            fname=name + str(i+1) + ".wav"
            subprocess.call(["mv", fname, path])
            # gt("mv %s %s" %(fname , path))        
        # GMMTraining.GMMModels('TrainingData/' , 'GMMModels')
        GMMTraining.singleModelTraining(path,'GMMModels')
        # print "press 1 to give passcode"
        return render(request, 'register.html', {'name':name, 'recorded' : True})
    if (name):
        return render(request, 'register.html', {'name':name, 'recorded' : False})
    else :
        return render(request, 'register.html')

def login(request):
    # print "press 1 to give passcode"
    # input()
    passRec = request.POST['passRec']
    recording("temp" , 1 , "",8)
    name = GMMTesting.testSingleaudio("temp1.wav")
    preprocessing.start("temp1.wav")
    print (name)
    
    
    #corr , offset  = recognition.start1('temp1.wav'  , "PasswordData/"+name+"/"+name+"1.wav")
    #corr , offset  = recognition.start('temp1.wav'  , "PasswordData/"+name+"/"+name+"1.wav")

    corr , offset  = recognition.start('temp1.wav'  , "PasswordData/"+name+"/"+name+"1.wav")
    corr , offset  = recognition.start('temp1.wav'  , "PasswordData/"+name+"/"+name+"2.wav")
    corr , offset  = recognition.start('temp1.wav'  , "PasswordData/"+name+"/"+name+"3.wav")
    corr , offset  = recognition.start('temp1.wav'  , "PasswordData/"+name+"/"+name+"4.wav")
    corr , offset  = recognition.start('temp1.wav'  , "PasswordData/"+name+"/"+name+"5.wav")
    
    # if corr > threshold :
    #     print "Hello " + name
    # else :
    #     print name
    #     print "Not Authenticated. Try Again!"
#        gt("rm temp1.wav")
    #authentication to be added