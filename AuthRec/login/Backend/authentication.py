import numpy as np
import scipy.io.wavfile as wavread

def compare(audiopath1, audiopath2 ):
	sr1 , audio1 = wavread.read(audiopath1)
	sr2 , audio2 = wavread.read(audiopath2)
	if audio1.ndim == 2 :
		audio1 = audio1[: , 1]
	if audio2.ndim == 2 :
		audio2 = audio2[: , 1]
	audio1=audio1/np.max(audio1)

	audio2=audio2/np.max(audio2)

	frame=1000
	minlen=min(len(audio1),len(audio2))
	i=0
	while (i<minlen) :
		arr1=audio1[i: minlen]
		arr2=audio2[i: minlen]
		i+=frame

		f1=np.fft.fft(arr1)
		f2=np.fft.fft(arr2)
		t = np.corrcoef(np.abs(f1) ,np.abs(f2))
	   
		corr=t[0][1]
		if(corr>0):
			print corr

compare('deepak1.wav','deepak3.wav')