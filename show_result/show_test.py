import sys
import glob
import os
import numpy as np
import matplotlib.pyplot as plt
from obspy.core import *
import get_pca
import get_ks

sys.path.append('../pick')

pca_win = 400
ks_win = 400
show_win = 7

fin = open('/home/zhangh/MyProject/FZHW/result_test.dat')
event = fin.readline()
record = fin.readline()
d_time = fin.readline()

while event:
    records = record.split(',')
    net, sta, time = records[0], records[1], records[2]
    y, m, d = time.split('T')[0].split('-')
    path = '/data2/ZSY_SAC/' + net + '/' + sta + '/' + y + '/' + m + '/' + d
    os.chdir(path)
    sts = glob.glob('*')
    st = read(sts[0])
    st += read(sts[1])
    st += read(sts[2])
    tp = UTCDateTime(time)
    t0 = float(d_time.split(' ')[1]) - 0.01
    st = st.slice(tp - show_win + t0, tp + show_win + t0).detrend('constant').filter('bandpass', freqmin=2, freqmax=15.)
    data_x = st[0].data
    data_y = st[1].data
    data_z = st[2].data
    pca = get_pca.get_pca(data_x, data_y, data_z, pca_win)
    kurtosis = get_ks.get_kurtosis(data_z, ks_win)
    skewness = get_ks.get_skewness(data_z, ks_win)
    t_fzhw = float(d_time.split(' ')[0]) - 0.01
    tp = float(d_time.split(' ')[1]) - 0.01
    title = net + ',' + sta + ',' + time
    timescale = np.arange(-show_win + pca_win / 100 + 2, show_win + 0.01, 0.01)

    p1 = plt.subplot(311)
    p1.plot(timescale, data_x[pca_win + 200:], lw=2)
    p1.set_ylabel('HHE', fontsize=20)
    p1.axvline(t_fzhw - tp, color='black', lw=2)
    p1.axvline(0, color='black', lw=2)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)

    p2 = plt.subplot(312)
    p2.plot(timescale, data_y[pca_win + 200:], lw=2)
    p2.set_ylabel('HHN', fontsize=20)
    p2.axvline(t_fzhw - tp, color='black', lw=2)
    p2.axvline(0, color='black', lw=2)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)

    p3 = plt.subplot(313)
    p3.plot(timescale, data_z[pca_win + 200:], lw=2)
    p3.set_xlabel('time/s', fontsize=20)
    p3.set_ylabel('HHZ', fontsize=20)
    p3.axvline(t_fzhw - tp, color='black', lw=2)
    p3.axvline(0, color='black', lw=2)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.show()
    event = fin.readline()
    record = fin.readline()
    d_time = fin.readline()

fin.close()
