import sys
import glob
import os
import numpy as np
import matplotlib.pyplot as plt
from obspy.core import *
import get_pca
import diff3

from scipy import signal

pca_win = 400
ks_win = 400
show_win = 5

fin = open('/home/zhangh/MyProject/FZHW/data/B16_phase.dat')
event = fin.readline()
record = fin.readline()

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
    st = st.slice(tp - show_win, tp + show_win).detrend('constant').filter('bandpass', freqmin=2, freqmax=15.)
    data_x = st[0].data
    data_y = st[1].data
    data_z = st[2].data
    pca = get_pca.get_pca(data_x, data_y, data_z, pca_win)
    b, a = signal.butter(8, 0.1, 'lowpass')
    pca_filter = signal.filtfilt(b, a, pca)
    pca_diff = diff3.diff3(pca_filter, 0.1)
    # kurtosis = get_ks.get_kurtosis(data_z,ks_win)
    # skewness = get_ks.get_skewness(data_z,ks_win)
    title = net + ',' + sta + ',' + time
    timescale = np.arange(-show_win + pca_win / 100, show_win - 1.99, 0.01)

    p1 = plt.subplot(211)
    p1.plot(timescale, pca_filter[:-201], lw=2)
    p1.set_ylabel('Polarization Degree', fontsize=16)

    p2 = plt.subplot(212)
    p2.plot(timescale, pca_diff[:-201], lw=2)
    p2.set_ylabel('Polarization Degree', fontsize=16)

    plt.show()
    event = fin.readline()
    record = fin.readline()

fin.close()
