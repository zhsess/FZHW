import numpy as np

def getK(data):
    n = len(data)
    x_bar = np.sum(data)/n
    sx = np.std(data)
    x4 = [(i-x_bar)**4 for i in data]
    K = np.sum(x4)/((n-1)*sx**4)-3
    return K

def getS(data):
    n = len(data)
    x_bar = np.sum(data)/n
    sx = np.std(data)
    x3 = [(i-x_bar)**3 for i in data]
    S = np.sum(x3)/((n-1)*sx**3)
    return S

def get_kurtosis(stz,k):
    l_s = len(stz)-k+1
    kurtosis = np.zeros(l_s)
    for i in range(l_s):
        kurtosis[i] = getK(stz[i:i+k])
    return kurtosis

def get_skewness(stz,k):
    l_s = len(stz)-k+1
    skewness = np.zeros(l_s)
    for i in range(l_s):
        skewness[i] = getS(stz[i:i+k])
    return skewness

        

    
