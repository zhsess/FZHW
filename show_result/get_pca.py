import numpy as np

def getPCA(dataMat):
    #meanVal = np.mean(dataMat,axis=0)
    #newData = dataMat - meanVal
    covMat = np.cov(dataMat)
    eigVals,eigVects = np.linalg.eig(np.mat(covMat))
    return eigVals,eigVects

def get_pca(stx,sty,stz,k):
    l_s = len(stx)-k+1
    pca = np.random.rand(l_s)
    for i in range(l_s):
        dataMat = np.mat([stx[i:i+k],sty[i:i+k],stz[i:i+k]])
        #dataMat = np.mat([stx[i:i+k],sty[i:i+k]])
        eigVals,eigVects = getPCA(dataMat)
        p,q=max(eigVals),np.sum(eigVals)-max(eigVals)
        pca[i] = 1-0.5*q/p
    return pca
    
    
