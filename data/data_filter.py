import os

sta_name = 'B16'
data_path = '/home/zhangh/Data/XJ_data/catalog/'
out_path = os.getcwd()
phase = open(data_path+'phase_zsy.dat')
event = open(data_path+'zsy.csv')
phase_out = open(out_path+'/'+sta_name+'_phase.dat','w')
event_out = open(out_path+'/'+sta_name+'_event.csv','w')
record = phase.readline()
while record:
    if record[0] == '2':
        event1 = event.readline() 
    else:
        sta = record.split(',')[1]
        if sta == sta_name:
            phase_out.write(event1)
            phase_out.write(record)
            event_out.write(event1)
    record = phase.readline()

phase.close()
event.close()
phase_out.close()
event_out.close()
