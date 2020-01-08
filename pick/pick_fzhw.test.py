import get_pca
import get_t
import get_ks
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
from obspy.core import *
from numba import jit

pca_win = 400
show_win = 10

phases = open('/home/zhangh/MyProject/FZHW/data/B16_phase.dat')
#events = open('/home/zhangh/MyProject/FZHW/data/B16_event.csv')
fout = open('/home/zhangh/MyProject/FZHW/data/B16_result.dat','w')
record = phases.readline()
num = 0
while record:
    num = num + 1
    print(num)
    if record[0] == '2':
        event = record
        record = phases.readline()
    else:
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
        st = st.slice(tp-show_win,tp+show_win).detrend('constant').filter('bandpass',freqmin=2.0,freqmax=15.0)
        datax = st[0].data
        datay = st[1].data
        dataz = st[2].data
        pca = get_pca.get_pca(datax,datay,dataz,pca_win)
        tmin,tleft,tright = get_t.get_t(pca,100*show_win-pca_win)
        if tmin-tleft >=10:
            min_value,left_value,right_value = pca[tmin],pca[tleft],pca[tright]
            k1 = (left_value-min_value)/(tmin-tleft)
            k2 = (right_value-min_value)/(tright-tmin)
            k3 = (right_value-min_value)/(left_value-min_value)
            m = k2/k1
            if k1>0.001 and 1.5*k1<k2 and left_value-min_value>0.07 and k3>1:
                tfzhw = int(tleft+pca_win-100*show_win)/100
                tpp = int(tmin+pca_win-100*show_win)/100
                tadd = int(tright+pca_win-100*show_win)/100
                fout.write(event)
                fout.write(record)
                fout.write(str(tfzhw)+' '+str(tpp)+' '+str(tadd)+'\n')
        record = phases.readline()
        record = phases.readline()
events.close()
phases.close()
fout.close()
ff.close()

