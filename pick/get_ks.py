import numpy as np


def get_K(data):
    n = len(data)
    x_bar = np.sum(data) / n
    sx = np.std(data)
    x4 = [(i - x_bar) ** 4 for i in data]
    K = np.sum(x4) / ((n - 1) * sx ** 4) - 3
    return K


def get_S(data):
    n = len(data)
    x_bar = np.sum(data) / n
    sx = np.std(data)
    x3 = [(i - x_bar) ** 3 for i in data]
    S = np.sum(x3) / ((n - 1) * sx ** 3)
    return S


def get_kurtosis(stz, k):
    l_s = len(stz) - k + 1
    kurtosis = np.zeros(l_s)
    for i in range(l_s):
        kurtosis[i] = get_K(stz[i:i + k])
    return kurtosis


def get_skewness(stz, k):
    l_s = len(stz) - k + 1
    skewness = np.zeros(l_s)
    for i in range(l_s):
        skewness[i] = get_S(stz[i:i + k])
    return skewness
