import numpy as np
# import commands as cmd
import subprocess
import scipy.io.wavfile as wvrd

#from statistics import variance

fng = 'FINGERPRINT='
threshold = 0.69

def covariance(f1 , f2 , l) :
    m1 = np.mean(f1)
    m2 = np.mean(f2)
    covr = 0
    for i in range(l) :
        covr = covr + (f1[i] - m1) * (f2[i] - m2)
    covr = covr / l 
    return covr
        

def correlation(f1, f2):
    if len(f1) > len(f2):
        f1 = f1[:len(f2)]
    else :
        f2 = f2[:len(f1)]
    
    
    # t = np.corrcoef(f1 ,f2)
    
    # return t[0][1]
    
    covariance = 0
    for i in range(len(f1)):
        covariance += 32 - bin(f1[i] ^ f2[i]).count("1")
    covariance = covariance / float(len(f1))
    
    return covariance/32
    
    # l = len(f1)
    # s1 = np.std(f1)
    # s2 = np.std(f2)
    # covr = covariance(f1 , f2 , l)
    # corr = covr / (s1 * s2)
    # return round(corr , 5)
    

def crosscorrelation(f1 , f2 , delay) :
    if delay < 0 :
        f2 = f2[-delay : ]
        f1 = f1[ : len(f2)]
    else :
        f1 = f1[delay : ]
        f2 = f2[ : len(f1)]
    
    return correlation(f1 , f2)

def similarity(f1 , f2 , span , step) :
#    print len(f1)
#    print len(f2)
    delayarray = np.arange(-span , span + 1 , step)
    #print delayarray
    crossarray = []
    for i in delayarray :
        tmp = crosscorrelation(f1 , f2 , i)
        crossarray.append(tmp)
    #print np.mean(crossarray)
    return np.array(crossarray)
    
        
def chromaFingerprint(path) :
    # chromaout = cmd.getoutput('fpcalc -raw %s' %(path))
    # subprocess.call("fpcalc -raw "+ path, shell=True)
    chromaout = subprocess.getoutput('fpcalc -raw '+path)
    ind = chromaout.find(fng) + len(fng)
    er = chromaout.find('ERROR')
    print(chromaout[ind : ])
    if (er < 0):
        chromaprints = map(int , chromaout[ind : ].split(','))
    else:
        chromaprints = map(int, [-1])
    return list(chromaprints)

def results(crossarray , span , step) :
    delayarray = np.arange(-span , span + 1 , step)
    ind = np.argmax(crossarray)
    corr = crossarray[ind]
    
    corr_mean = np.mean(crossarray)
    
    if corr == 1 :
        print ('Successfully authenticated with correlation %.4f' %(corr) )
        return corr , delayarray[ind] , True
    if corr >= threshold :
        print ('Successfully authenticated with correlation %.4f %.4f' %(corr , corr_mean) )
        return corr_mean , delayarray[ind], True
    print ('Not Authenticated')
#    print corr
    return corr , delayarray[ind], False

def start(rec , save , step = 1) : 
    recprints = chromaFingerprint(rec)
    saveprints = chromaFingerprint(save)
    span = min(len(recprints) , len(saveprints)) - 1
    crossarray =  similarity(recprints , saveprints , span , step)
#    print np.var(crossarray)
    return results(crossarray , span , step)

def start1(rec1 , rec2) :
    samplerate , f1 = wvrd.read(rec1)
    if f1.ndim == 2 :
        f1 = f1[: , 1]
    
    samplerate , f2 = wvrd.read(rec2)
    if f2.ndim == 2 :
        f2 = f2[: , 1]
    print (f1)
    span = min(len(f1) , len(f2)) - 1
    crossarray = similarity(f1 , f2 , span , 10)
    return results(crossarray, span, 1)

#start('temp2.wav' , 'PasswordData/rahul/rahul5.wav')
#start1('Utkarsh4.wav','PasswordData/Utkarsh/Utkarsh3.wav')