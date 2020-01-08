import matplotlib.pyplot as plt
import numpy as np
import os
import glob
from obspy.core import *

#stla = 25.9244
show_win = 1.5
stla = 25.02388
stlo = 103.0541
stamp = 1.859
fin = open('/home/zhangh/MyProject/FZHW/aid/B16_result.dat')

dt = []
dist = []

event = fin.readline()
phase = fin.readline()
phase_time = fin.readline()
timeline = np.arange(-1,1.51,0.01)
fig = plt.subplot(111)
while event:
    dla = float(event.split(',')[1])-stla
    dlo = float(event.split(',')[2])-stlo
    deep = float(event.split(',')[3])+stamp
    dt = float(phase_time.split(' ')[1])-float(phase_time.split(' ')[0])
    dist0 = np.sqrt((dla**2+dlo**2*np.cos(stla))*111**2+deep**2)
    if float(event.split(',')[2])>103:
        net,sta,time = phase.split(',')[0],phase.split(',')[1],phase.split(',')[2]
        y,m,d = time.split('T')[0].split('-')
        path = '/data2/ZSY_SAC/'+net+'/'+sta+'/'+y+'/'+m+'/'+d
        os.chdir(path)
        sts = glob.glob('*')
        st = read(sts[2])

        t0 = UTCDateTime(time)
        tp = t0 + float(phase_time.split(' ')[1])
        tfzhw = t0 + float(phase_time.split(' ')[0])
        st = st.slice(tp-1,tp+show_win).detrend('constant').filter('bandpass',freqmin=2.,freqmax=15)
        dataz = st[0].data
        dataz = dataz/max(max(dataz),-min(dataz))
        if dla>=0:
            dataz = [i*5+dist0 for i in dataz]
            fig.plot(timeline,dataz,'b')
            fig.plot(-dt,dataz[100-int(100*dt)],'r*',markersize=10)
    event = fin.readline()
    phase = fin.readline()
    phase_time = fin.readline()
fig.set_xlabel('Time Difference/s',fontsize=15)
fig.set_ylabel('Along Fault Distance/km',fontsize=15)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
fig.axvline(0,color='black')
plt.show()

fin.close()
