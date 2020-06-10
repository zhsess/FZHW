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
# events = open('/home/zhangh/MyProject/FZHW/data/B16_event.csv')
f_out = open('/home/zhangh/MyProject/FZHW/data/B16_result.dat', 'w')
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
        net, sta, time = records[0], records[1], records[2]
        y, m, d = time.split('T')[0].split('-')
        path = '/data2/ZSY_SAC/' + net + '/' + sta + '/' + y + '/' + m + '/' + d
        os.chdir(path)
        sts = glob.glob('*')
        st = read(sts[0])
        st += read(sts[1])
        st += read(sts[2])
        tp = UTCDateTime(time)
        st = st.slice(tp - show_win, tp + show_win).detrend('constant').filter('bandpass', freqmin=2.0, freqmax=15.0)
        data_x = st[0].data
        data_y = st[1].data
        data_z = st[2].data
        pca = get_pca.get_pca(data_x, data_y, data_z, pca_win)
        t_min, t_left, t_right = get_t.get_t(pca, 100 * show_win - pca_win)
        if t_min - t_left >= 10:
            min_value, left_value, right_value = pca[t_min], pca[t_left], pca[t_right]
            k1 = (left_value - min_value) / (t_min - t_left)
            k2 = (right_value - min_value) / (t_right - t_min)
            k3 = (right_value - min_value) / (left_value - min_value)
            m = k2 / k1
            if k1 > 0.001 and 1.5 * k1 < k2 and left_value - min_value > 0.07 and k3 > 1:
                t_fzhw = int(t_left + pca_win - 100 * show_win) / 100
                tpp = int(t_min + pca_win - 100 * show_win) / 100
                tadd = int(t_right + pca_win - 100 * show_win) / 100
                f_out.write(event)
                f_out.write(record)
                f_out.write(str(t_fzhw) + ' ' + str(tpp) + ' ' + str(tadd) + '\n')
        record = phases.readline()
        record = phases.readline()
# events.close()
phases.close()
f_out.close()
