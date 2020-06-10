import get_ks
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
import diff3
from obspy.core import *
from numba import jit

ks_win = 500

fin = open('/home/zhangh/MyProject/FZHW/pick_ross/result.dat')
event = fin.readline()
phase = fin.readline()
tp = fin.readline()
num = 0
while phase:
    num = num + 1
    tp = float(tp)
    print(tp)
    records = phase.split(',')
    net, sta, time = records[0], records[1], records[2]
    y, m, d = time.split('T')[0].split('-')
    path = '/data2/ZSY_SAC/' + net + '/' + sta + '/' + y + '/' + m + '/' + d
    os.chdir(path)
    sts = glob.glob('*Z.SAC')
    st = read(sts[0])
    t0 = UTCDateTime(time)
    st = st.slice(t0 - 6.19, t0 + 2).detrend('constant').filter('highpass', freq=1.0)
    t_scale = np.linspace(-1.2, 2, 321)
    data_z = st[0].data
    kurt = get_ks.get_kurtosis(data_z, ks_win)
    skew = get_ks.get_skewness(data_z, ks_win)

    kurt_d = diff3.diff(kurt, 0.01)
    skew_d = diff3.diff(skew, 0.01)

    p1 = plt.subplot(311)
    plt.title(net + sta + time)
    p1.plot(t_scale, data_z[499:])
    p1.axvline(tp, color='black', lw=1)
    p1.axvline(0, color='black', lw=1)
    p2 = plt.subplot(312)
    p2.plot(t_scale, kurt_d)
    p2.axvline(tp, color='black', lw=1)
    p2.axvline(0, color='black', lw=1)
    p3 = plt.subplot(313)
    p3.plot(t_scale, skew_d)
    p3.axvline(tp, color='black', lw=1)
    p3.axvline(0, color='black', lw=1)
    plt.show()
    event = fin.readline()
    phase = fin.readline()
    tp = fin.readline()
fin.close()
