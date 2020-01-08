import numpy as np
import matplotlib.pyplot as plt
import os
import glob
from obspy.core import *

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
    t0 = float(dtime.split(' ')[1])
    st = st.slice(tp+t0-5,tp+t0+7).detrend('constant').filter('bandpass',freqmin=2,freqmax=10.)
    datax = st[0].data
    datay = st[1].data
    dataz = st[2].data
    tfzhw = int(100*(float(dtime.split(' ')[0])-float(dtime.split(' ')[1])))+500
    tp = 500
    ts = 800
    plt.subplot(111)
    #plt.plot(datay[tfzhw-100:tfzhw],-datax[tfzhw-100:tfzhw],'b',linewidth=2)
    #plt.plot(datay[tfzhw:492],-datax[tfzhw:492],'b',linewidth=2)
    #plt.plot(-datay[492:tp],-datax[492:tp],'b',linewidth=2)
    #plt.plot([datay[491],-datay[492]],[-datax[491],-datax[492]],'b',linewidth=2)
    #plt.plot(datay[tp:tp+60],-datax[tp:tp+60],'b',linewidth=2)
    plt.plot(datay[ts:ts+60],-datax[ts:ts+60],'b',linewidth=2)
    plt.axis("equal")
    plt.show()
    event = fin.readline()
    record = fin.readline()
    dtime = fin.readline()

fin.close()



