import numpy as np
import matplotlib.pyplot as plt
import os
import glob
from obspy.core import *

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
    t0 = float(d_time.split(' ')[1])
    st = st.slice(tp + t0 - 5, tp + t0 + 7).detrend('constant').filter('bandpass', freqmin=2, freqmax=10.)
    data_x = st[0].data
    data_y = st[1].data
    data_z = st[2].data
    t_fzhw = int(100 * (float(d_time.split(' ')[0]) - float(d_time.split(' ')[1]))) + 500
    tp = 500
    ts = 800
    plt.subplot(111)
    # plt.plot(data_y[t_fzhw-100:t_fzhw],-data_x[t_fzhw-100:t_fzhw],'b',linewidth=2)
    # plt.plot(data_y[t_fzhw:492],-data_x[t_fzhw:492],'b',linewidth=2)
    # plt.plot(-data_y[492:tp],-data_x[492:tp],'b',linewidth=2)
    # plt.plot([data_y[491],-data_y[492]],[-data_x[491],-data_x[492]],'b',linewidth=2)
    # plt.plot(data_y[tp:tp+60],-data_x[tp:tp+60],'b',linewidth=2)
    plt.plot(data_y[ts:ts + 60], -data_x[ts:ts + 60], 'b', linewidth=2)
    plt.axis("equal")
    plt.show()
    event = fin.readline()
    record = fin.readline()
    d_time = fin.readline()

fin.close()
