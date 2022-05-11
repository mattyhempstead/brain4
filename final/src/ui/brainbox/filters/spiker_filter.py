from scipy import signal
import numpy as np

# Butterworth filter
def LP_Filter(rawData):
    Fs = 10000
    order = 5
    cutOff = 7 # Hz
    b, a = signal.butter(order, Wn=cutOff/(Fs/2)) 
    # Zero Phase double filter
    filteredSignal = signal.filtfilt(b, a, rawData)
    return filteredSignal

 #Convert spikerBox data to list of amplitude measurements
def process_data(dataIn):
    rawData = np.array(dataIn)
    processedData = []
    i = 1
    while i < len(rawData) - 1:
        if rawData[i] > 127:
            intOut = (np.bitwise_and(rawData[i], 127)) * 128
            i += 1
            intOut += rawData[i]
            processedData = np.append(processedData, intOut)
        i += 1
    return processedData
