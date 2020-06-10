import numpy as np
f_in = open('/home/zhangh/MyProject/FZHW/aid/B16_result')
f_out = open('/home/zhangh/MyProject/FZHW/aid/B16_loc.dat', 'w')
event = f_in.readline()
while event:
    time, la, lo, d, m = event.split(',')
    x = 100*(float(lo)-103)
    y = 111*(float(la)-25)
    l2 = (111*x-25*y)**2/(111**2+25**2)
    dis = np.sqrt(x**2+y**2-l2)
    print(dis)
    dis = int(100*dis)/100
    f_out.write(str(dis)+' -'+d+' '+m)
    for times in range(3):
        event = f_in.readline()
f_in.close()
f_out.close()
