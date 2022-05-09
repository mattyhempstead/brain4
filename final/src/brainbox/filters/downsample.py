import numpy as np

def mean(arr, factor=100):
    """
    Mean downsample by a factor of n

    e.g. factor=100 will scale down 100x
    """
    end =  factor * int(len(arr)/factor)
    return np.mean(arr[:end].reshape(-1, factor), 1)
