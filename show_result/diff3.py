def diff(data,delta):
    result = [0]*len(data)
    result[0] = (data[1]-data[0])/delta
    for i in range(1,len(data)-1):
        result[i] = (data[i+1]-data[i-1])/(2*delta)
    result[-1] = (data[-1]-data[-2])/delta
    return result

def diff3(data,delta):
    result = diff(data,delta)
    result = diff(result,delta)
    result = diff(result,delta)
    return result
