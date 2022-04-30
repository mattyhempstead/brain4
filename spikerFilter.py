from scipy import signal

# Butterworth filter
def LP_Filter(rawData):
    Fs = 10000
    order = 5
    cutOff = 7 # Hz
    normalizedCutOff = cutOff/Fs
    b, a = signal.butter(order, Wn=normalizedCutOff) 
    # Zero Phase double filter
    filteredSignal = signal.filtfilt(b, a, rawData)
    return filteredSignal



