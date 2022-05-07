import numpy as np

def mean(arr, factor=n):
    """
    Mean downsample by a factor of n

    e.g. factor=100 will scale down 100x
    """
    end =  n * int(len(arr)/n)
    return np.mean(arr[:end].reshape(-1, n), 1)
