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
import time


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
    elif (val == 2):
        return render(request,'register.html')
    else :
        return render(request,'password.html')

def register(request):
    name = request.POST['name']
    record = request.POST['record']
    dur = request.POST['dur']
    passRecord = request.POST['pass']
    if (name and record and dur):
        dur = int(dur)
        # name = raw_input()
        # passpath = "PasswordData/"+name
        # print "give pass duration:"
        passpath = "login/Backend/PasswordData/"+name

        time.sleep(1)
        recording(name + '1.wav',10,passpath,dur)
        preprocessing.start(name+"1.wav")
        subprocess.call(["mv", name+"1.wav", passpath])
        
        time.sleep(1)
        recording(name + '2.wav',10,passpath,dur)
        preprocessing.start(name+"2.wav")
        subprocess.call(["mv", name+"2.wav", passpath])
        
        time.sleep(1)
        recording(name + '3.wav',10,passpath,dur)
        preprocessing.start(name+"3.wav")
        subprocess.call(["mv", name+"3.wav", passpath])

        time.sleep(1)
        recording(name + '4.wav',10,passpath,dur)
        preprocessing.start(name+"4.wav")
        subprocess.call(["mv", name+"4.wav", passpath])
        
        time.sleep(1)
        recording(name + '5.wav',10,passpath,dur)
        preprocessing.start(name+"5.wav")
        subprocess.call(["mv", name+"5.wav", passpath])
        
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
    passRec = request.POST['passRec']
    recording("temp" , 1 , "",8)
    name = GMMTesting.testSingleaudio("temp1.wav")
    preprocessing.start("temp1.wav")
    print (name)
    result = False

    corr1   = recognition.start('temp1.wav'  , "login/Backend/PasswordData/"+name+"/"+name+"1.wav")
    corr2   = recognition.start('temp1.wav'  , "login/Backend/PasswordData/"+name+"/"+name+"2.wav")
    corr3   = recognition.start('temp1.wav'  , "login/Backend/PasswordData/"+name+"/"+name+"3.wav")
    corr4   = recognition.start('temp1.wav'  , "login/Backend/PasswordData/"+name+"/"+name+"4.wav")
    corr5   = recognition.start('temp1.wav'  , "login/Backend/PasswordData/"+name+"/"+name+"5.wav")

    confirm=0
    confirm=corr1+corr2+corr3+corr4+corr5
    if confirm > 2 :
        result = True
    return render(request, 'result.html',{'name':name, 'result' : result})

def changePass(request):
    name = request.POST['name']
    dur = request.POST['dur']

    if(name and dur):
        dur = int(dur)
        # name = raw_input()
        # passpath = "PasswordData/"+name
        # print "give pass duration:"
        passpath = "login/Backend/PasswordData/"+name

        time.sleep(1)
        recording(name + '1.wav',10,passpath,dur)
        preprocessing.start(name+"1.wav")
        subprocess.call(["mv", name+"1.wav", passpath])
        
        time.sleep(1)
        recording(name + '2.wav',10,passpath,dur)
        preprocessing.start(name+"2.wav")
        subprocess.call(["mv", name+"2.wav", passpath])
        
        time.sleep(1)
        recording(name + '3.wav',10,passpath,dur)
        preprocessing.start(name+"3.wav")
        subprocess.call(["mv", name+"3.wav", passpath])

        time.sleep(1)
        recording(name + '4.wav',10,passpath,dur)
        preprocessing.start(name+"4.wav")
        subprocess.call(["mv", name+"4.wav", passpath])
        
        time.sleep(1)
        recording(name + '5.wav',10,passpath,dur)
        preprocessing.start(name+"5.wav")
        subprocess.call(["mv", name+"5.wav", passpath])

        return render(request,'home.html')

    if (name):
        return render(request, 'password.html', {'name':name })
    else: 
        return render(request, 'password.html')