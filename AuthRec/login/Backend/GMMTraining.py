import numpy as np
from scipy.io.wavfile import read as rd
from sklearn.mixture import GaussianMixture as GMM
from .featureextraction import extract_features
import os
from .Models import saveModels

def GMMModels(audiopath , modeldest) :
    for folder in os.listdir(audiopath) :
        mfcc_features = np.asarray(())
        for audio in os.listdir(audiopath + folder) :
            samplerate , audiofile = rd(audiopath + folder + '/' + audio)
            tmp   = extract_features(audiofile,samplerate)
            if mfcc_features.size == 0 :
                mfcc_features = tmp
            else :
                mfcc_features = np.vstack((mfcc_features , tmp))
        
        gmm = GMM(n_components = 16, max_iter = 200, covariance_type='diag',n_init = 3)
        gmm.fit(mfcc_features)
        saveModels(modeldest , gmm , folder)
        

#GMMModels('TrainingData/' , 'GMMModels')
def singleModelTraining(audiopath,modeldest):
    mfcc_features = np.asarray(())
    for folder in os.listdir(audiopath):
        samplerate , audiofile = rd(audiopath + '/'+folder )
        tmp   = extract_features(audiofile,samplerate)
        if mfcc_features.size == 0 :
            mfcc_features = tmp
        else :
            mfcc_features = np.vstack((mfcc_features , tmp))
    gmm = GMM(n_components = 16, max_iter = 200, covariance_type='diag',n_init = 3)
    gmm.fit(mfcc_features)
    saveModels(modeldest , gmm , audiopath[27:])