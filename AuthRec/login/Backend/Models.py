import _pickle as cPickle

def saveModels(path , model , name) :
    path = 'login/Backend/' + path
    path = path + '/' + name + '.gmm'
    cPickle.dump(model , open(path , 'wb'))
    
    # print ('Saved for ' + name)
    
def retrieveModels(modelname) :
    return cPickle.load(open(modelname , 'rb'))
    