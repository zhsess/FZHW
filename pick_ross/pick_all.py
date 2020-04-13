import get_ks
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
import diff3
from obspy.core import *
from numba import jit

ks_win = 500

fin1 = open('/home/zhangh/Data/XJ_data/catalog/phase_zsy.dat')
fin2 = open('/home/zhangh/Data/XJ_data/catalog/zsy.csv')
fout = open('/home/zhangh/MyProject/FZHW/pick_ross/result.dat','w')
record = fin1.readline()
num = 0
while record:
    num = num + 1
    print(num)
    if record[0] == '2':
        event = fin2.readline()
        record = fin1.readline()
    else:
        records = record.split(',')
        net,sta,time = records[0],records[1],records[2]
        y,m,d = time.split('T')[0].split('-')
        path = '/data2/ZSY_SAC/'+net+'/'+sta+'/'+y+'/'+m+'/'+d
        os.chdir(path)
        sts = glob.glob('*Z.SAC')
        st = read(sts[0])
        t0 = UTCDateTime(time)
        st = st.slice(t0-5.19,t0+1).detrend('constant').filter('highpass',freq=1.0)
        t_scale = np.linspace(-0.2,1,121)
        dataz = st[0].data
        kurt = get_ks.get_kurtosis(dataz,ks_win)
        skew = get_ks.get_skewness(dataz,ks_win)
        kurt_d = diff3.diff(kurt,0.01)
        kurt_d_abs = [abs(i) for i in kurt_d]
        skew_d = diff3.diff(skew,0.01)
        skew_d_abs = [abs(i) for i in skew_d]

        kmax = kurt_d_abs.index(max(kurt_d_abs))
        smax = skew_d_abs.index(max(skew_d_abs))
        if abs(kmax-smax)<4:
            i =smax
            while skew_d[i]*skew_d[i-1]>0:
                i = i-1
            if abs(skew_d[i])>abs(skew_d[i-1]):
                tp = i
            else:
                tp = i-1
            tp = round(tp/100-0.2,2)
            if tp>0.05:
                fout.write(event)
                fout.write(record)
                fout.write(str(tp)+'\n')
        record = fin1.readline()
fin1.close()
fin2.close()
fout.close()

