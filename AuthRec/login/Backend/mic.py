import os
import time
import playsound
import speech_recognition as sr
from gtts import gTTS
import sounddevice

from scipy.io.wavfile import write

def speak(text):
	tts=gTTS(text=text, lang='en')
	filename= "voice.mp3"
	tts.save(filename)
	playsound.playsound(filename)


def get_audio():
	r=sr.Recognizer()
	with sr.Microphone() as source:
		audio =r.listen(source)
		print(type(audio))
		said= ""

		try:
			said =r.recognize_google(audio)
			print(said)
		except Exception as e:
			print("Exception: "+str(e))
	return said


print("Select Option:\n1. New user\t 2.Existing User")
a=input();
a=int(a)
if(a!=1) :
	print(a)
else:

	print("We will take 3 sample. Press 1 to start recording")
	input()
	sr=44100
	second=6
	for i in range(3):
		print(str(i)+" recording....")
		record_voice=sounddevice.rec(int(second * sr),samplerate=sr,channels=2)
		sounddevice.wait()
		fname="record"+str(i)+".wav"
		write(fname,sr,record_voice)
		print(str(i)+" recognition done")



# speak("hello deepak")
# get_audio()