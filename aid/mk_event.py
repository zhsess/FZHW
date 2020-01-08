import numpy as np
fin = open('/home/zhangh/MyProject/FZHW/aid/B16_result')
fout = open('/home/zhangh/MyProject/FZHW/aid/B16_loc.dat','w')
event = fin.readline()
while event:
    time,la,lo,d,m = event.split(',')
    x = 100*(float(lo)-103)
    y = 111*(float(la)-25)
    l2 = (111*x-25*y)**2/(111**2+25**2)
    dis = np.sqrt(x**2+y**2-l2)
    print(dis)
    dis = int(100*dis)/100
    fout.write(str(dis)+' -'+d+' '+m)
    event = fin.readline()
    event = fin.readline()
    event = fin.readline()
fin.close()
fout.close()
