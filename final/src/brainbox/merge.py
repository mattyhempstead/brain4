from xml.dom.minidom import getDOMImplementation
import serial 
import numpy as np
import Filters.spikerFilter
import pandas as pd

import time

def average(arr, n):
    end =  n * int(len(arr)/n)
    return np.mean(arr[:end].reshape(-1, n), 1)


# Read unprocessed data from spikerBox
def read_arduino(ser, inputBufferSize):
    data = ser.read(inputBufferSize)
    out = [(int(data[i])) for i in range(0,len(data))]
    return out

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


# For buffer size of 2000, each buffer contains 0.1s of data, so 3 s = 30 loops
class stream():
    def __init__(self, inputBufferSize, dataTime):
        self.bufferSize = inputBufferSize
        self.numLoop = dataTime/(inputBufferSize/20000)
        self.bRate = 230400
        self.portNum = '/dev/tty.usbserial-DJ00E33Q'
        self.Fs = 10000 
        self.arraySize = 60000
        self.bufferFillTime = inputBufferSize/20000.0

        self.start_time = time.perf_counter()

    def getData(self): # Get one buffer worth of data 0.1s for
        dataActual = []
        ser = serial.Serial(port=self.portNum, baudrate=self.bRate)
        ser.timeout = self.bufferSize/20000.0
        try:
            while True:
                data = read_arduino(ser, self.bufferSize)
                dataTemp = process_data(data)
                dataActual = np.append(dataActual, dataTemp)
                # Truncate array 
                dataActual = dataActual[-self.arraySize:]
                if len(dataActual) == self.arraySize:
                    filteredArray = Filters.spikerFilter.LP_Filter(dataActual)
                    print(len(filteredArray), filteredArray)
                    downArr = average(filteredArray, 100)
                    print(len(downArr))
                    print(time.perf_counter() - self.start_time)
                    self.start_time = time.perf_counter()
                    

                    

                    # Filter if needed
                    # Downsample
                    # Classify
                        # Send signal to UI if needed

                #if len(dataActual) > self.bufferSize*self.numLoop:
                    #print(dataTemp[-int(self.bufferSize*self.numLoop)])
        except KeyboardInterrupt:
            return dataActual

a = stream(2000, 3)
a.getData()



