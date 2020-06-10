import get_ks
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
import diff3
from obspy.core import *
from numba import jit

ks_win = 500

fin = open('/home/zhangh/MyProject/FZHW/data/B16_phase.dat')
# events = open('/home/zhangh/MyProject/FZHW/data/B16_event.csv')
f_out = open('/home/zhangh/MyProject/FZHW/pick_ross/B16_result.dat', 'w')
event = fin.readline()
phase = fin.readline()
num = 0
while event:
    num = num + 1
    print(num)
    records = phase.split(',')
    net, sta, time = records[0], records[1], records[2]
    y, m, d = time.split('T')[0].split('-')
    path = '/data2/ZSY_SAC/' + net + '/' + sta + '/' + y + '/' + m + '/' + d
    os.chdir(path)
    sts = glob.glob('*Z.SAC')
    st = read(sts[0])
    t0 = UTCDateTime(time)
    st = st.slice(t0 - 5.19, t0 + 1).detrend('constant').filter('highpass', freq=1.0)
    t_scale = np.linspace(-0.2, 1, 121)
    data_z = st[0].data
    kurt = get_ks.get_kurtosis(data_z, ks_win)
    skew = get_ks.get_skewness(data_z, ks_win)

    kurt_d = diff3.diff(kurt, 0.01)
    kurt_d_abs = [abs(i) for i in kurt_d]
    skew_d = diff3.diff(skew, 0.01)
    skew_d_abs = [abs(i) for i in skew_d]

    k_max = kurt_d_abs.index(max(kurt_d_abs))
    s_max = skew_d_abs.index(max(skew_d_abs))
    if abs(k_max - s_max) < 4:
        i = s_max
        while skew_d[i] * skew_d[i - 1] > 0:
            i = i - 1
        if abs(skew_d[i]) > abs(skew_d[i - 1]):
            tp = i
        else:
            tp = i - 1
        tp = round(tp / 100 - 0.2, 2)
        f_out.write(phase)
        f_out.write(str(tp) + '\n')
    event = fin.readline()
    phase = fin.readline()
fin.close()
f_out.close()
