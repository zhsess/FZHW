import os

path = os.getcwd()

sta_name = 'B16'
result = open(path + '/result.dat')
output = open(path + '/' + sta_name + '_result.dat', 'w')

record1 = result.readline()
record2 = result.readline()
record3 = result.readline()
while record1:
    sta = record2.split(',')[1]
    if sta == sta_name:
        output.write(record1 + record2 + record3)
    record1 = result.readline()
    record2 = result.readline()
    record3 = result.readline()
result.close()
output.close()
