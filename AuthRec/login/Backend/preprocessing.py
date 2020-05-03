import numpy as np
import scipy.io.wavfile as wvrd
import matplotlib.pyplot as plt
import wave


def removeSilence(audio) :
    window_size = 160
    factor = 0.1
    threshold = 0
    adaptive_th = 0
    n = 0
    counter = 0
    audio_out = np.array([] , dtype = np.int16)
    
    while len(audio) >= window_size :
        current_frame = audio[:window_size] ** 2
        #print current_frame
        audio = audio[window_size:]    
        
        threshold = np.min(current_frame) + (np.ptp(current_frame) * factor)
        adaptive_th = (adaptive_th * n + threshold ) / (1. + n)
        #print adaptive_th
        
        if adaptive_th >= np.mean(current_frame) :
            counter = counter + 1
        else :
            counter = 0
        
        if counter <= 20 :
            audio_out = np.append(audio_out , audio[:window_size])
        
        n = n + 1
        
    for i in range(len(audio_out)) :
        if audio_out[i] ** 2 > 1e-3 :
            audio_out = audio_out[i:]
            return audio_out
    
   
    

def start(audiopath) :
    samplerate , audio = wvrd.read(audiopath)
    print(audio)
    if audio.ndim == 2 :
        audio = audio[: , 1]
    # plt.figure()
    # plt.plot(audio)
    # plt.show()
    audio = removeSilence(audio)
    print(audiopath)
    # plt.figure()
    # plt.plot(audio)
    # plt.show()
    wvrd.write(audiopath, samplerate, audio)    
    




