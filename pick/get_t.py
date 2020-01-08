import numpy as np

'''
def get_pca_d(stx):
    stx_d = np.random.rand(len(stx)-1)
    for i in range(len(stx)-1):
        stx_d[i] = stx[i+1]-stx[i]
    return stx_d

def stp(st):
    short_win = 10
    result = np.random.rand(len(st)-2*short_win)
    for i in range(len(result)):
        left_sum,right_sum=0,0
        for j in range(5):
             left_sum = left_sum + st[i+j]**2
             right_sum = right_sum + st[i+j+5]**2
             result[i] = right_sum/left_sum
    return result
def ltp(st):
    l = len(st)
    short_win = 5
    result = np.random.rand(len(st)-2*short_win)
    for i in range(len(result)):
        left_sum,right_sum=0,0
        for j in st[:i+short_win]:
             left_sum = left_sum + j**2
        for j in st[i+short_win+10:]:
             right_sum = right_sum + j**2
        result[i] = right_sum*(i+short_win)/(left_sum*(l-i-short_win))
    return result
'''
def get_t(stx,t0):
    stx = stx.tolist()
    min_win = 100
    max_win_right,max_win_left = 80,100
    st_min = stx[t0-min_win:t0+min_win]
    for i in range(2*(min_win)):
        st_min[i]=st_min[i]-i/800
    min_value = min(st_min)
    min_t = st_min.index(min_value)
    min_t_abs = t0-min_win+min_t
    #left_max
    pca_left = stx[min_t_abs-max_win_left:min_t_abs]
    for i in range(max_win_left):
        pca_left[i] = pca_left[i]+i/600
    max_t_left = pca_left.index(max(pca_left))+min_t_abs-max_win_left
    #right_max
    pca_right = stx[min_t_abs:min_t_abs+max_win_right]
    for i in range(max_win_right):
        pca_right[i] = pca_right[i]-i/800
    max_t_right = pca_right.index(max(pca_right))+min_t_abs
    return min_t_abs,max_t_left,max_t_right     
    
