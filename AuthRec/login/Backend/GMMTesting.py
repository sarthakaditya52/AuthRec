import numpy as np
from scipy.io.wavfile import read as rd
from sklearn.mixture import GaussianMixture as GMM
from .featureextraction import extract_features
import os
from .Models import retrieveModels

models=[]
models_name=[]

def testSingleaudio(testpath) :
    samplerate , audiofile = rd(testpath)
    mfcc_features = extract_features(audiofile , samplerate)
    maxscore = -999999
    speaker = ""
    for model in os.listdir('login/Backend/GMMModels/') :
        # print model
        tmp = retrieveModels('login/Backend/GMMModels/' + model)
        score = tmp.score(mfcc_features)
        if score > maxscore :
            maxscore = score
            speaker = model.split(".gmm")[0]
        # print tmp.score(mfcc_features)
    return speaker

def testDataSet(datasetpath,succes_rate) :
    for model in os.listdir('login/Backend/GMMModels/') :
        models_name.append(model)
        tmp = retrieveModels('login/Backend/GMMModels/' + model)
        models.append(tmp)
    total_files = 0
    for folder in os.listdir(datasetpath) :
    	for audio in os.listdir(datasetpath + folder) :
    		total_files += 1
    		samplerate , audiofile = rd(datasetpath + folder + '/'+audio)
    		mfcc_features = extract_features(audiofile , samplerate)
    		max_score=-999999
    		max_model=models[0]
    		i=0
    		for model in models :
    			score = model.score(mfcc_features)
    			if score > max_score :
    				max_score = score
    				max_model = models_name[i]
    			i = i + 1
    		
    		# print audio
    		# print max_model
    		# print max_score
    		# print "---------------------------------"

    		if max_model[:len(max_model)-4]== folder:
    			succes_rate+=1
    succes_rate = (succes_rate*1.00) / total_files
    print (str((succes_rate)*100)+ "%")


#testDataSet('TestingData/',0)
