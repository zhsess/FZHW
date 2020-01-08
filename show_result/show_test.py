import sys
import glob
import os
sys.path.append('../pick')
import numpy as np
import matplotlib.pyplot as plt
from obspy.core import *
import get_pca
import get_ks

pca_win = 400
ks_win = 400
show_win =7 

fin  = open('/home/zhangh/MyProject/FZHW/result_test.dat')
event = fin.readline()
record = fin.readline()
dtime = fin.readline()

while event:
    records = record.split(',')
    net,sta,time = records[0],records[1],records[2]
    y,m,d = time.split('T')[0].split('-')
    path = '/data2/ZSY_SAC/'+net+'/'+sta+'/'+y+'/'+m+'/'+d
    os.chdir(path)
    sts = glob.glob('*')
    st = read(sts[0])
    st += read(sts[1])
    st += read(sts[2])
    tp = UTCDateTime(time)
    t0 = float(dtime.split(' ')[1])-0.01
    st = st.slice(tp-show_win+t0,tp+show_win+t0).detrend('constant').filter('bandpass',freqmin=2,freqmax=15.)
    datax = st[0].data
    datay = st[1].data
    dataz = st[2].data
    pca = get_pca.get_pca(datax,datay,dataz,pca_win)
    kurtosis = get_ks.get_kurtosis(dataz,ks_win)
    skewness = get_ks.get_skewness(dataz,ks_win)
    tfzhw = float(dtime.split(' ')[0])-0.01
    tp = float(dtime.split(' ')[1])-0.01
    title = net+','+sta+','+time
    timescale = np.arange(-show_win+pca_win/100+2,show_win+0.01,0.01)
    
    p1 = plt.subplot(311)
    p1.plot(timescale,datax[pca_win+200:],lw=2)
    p1.set_ylabel('HHE',fontsize=20)
    p1.axvline(tfzhw-tp,color='black',lw=2)
    p1.axvline(0,color='black',lw=2)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    
    p2 = plt.subplot(312)
    p2.plot(timescale,datay[pca_win+200:],lw=2)
    p2.set_ylabel('HHN',fontsize=20)
    p2.axvline(tfzhw-tp,color='black',lw=2)
    p2.axvline(0,color='black',lw=2)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)

    p3 = plt.subplot(313)
    p3.plot(timescale,dataz[pca_win+200:],lw=2)
    p3.set_xlabel('time/s',fontsize=20)
    p3.set_ylabel('HHZ',fontsize=20)
    p3.axvline(tfzhw-tp,color='black',lw=2)
    p3.axvline(0,color='black',lw=2)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.show()
    event = fin.readline()
    record = fin.readline()
    dtime = fin.readline()

fin.close()



