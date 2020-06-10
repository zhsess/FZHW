f_in = open('/home/zhangh/MyProject/FZHW/aid/B16_result.dat')
f_out = open('/home/zhangh/MyProject/FZHW/aid/B16_loc.dat', 'w')
event = f_in.readline()
while event:
    time, la, lo, d, m = event.split(',')
    f_out.write(lo+' '+la+' '+m.split('\n')[0]+' '+d+'\n')
    for times in range(3):
        event = f_in.readline()
f_in.close()
f_out.close()
