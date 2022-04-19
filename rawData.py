import serial 
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from scipy.io.wavfile import write


# Read unprocessed data from spikerBox
def read_arduino(ser, inputBufferSize):
    data = ser.read(inputBufferSize)
    out = [(int(data[i])) for i in range(0,len(data))]
    return out

# Convert spikerBox data to list of amplitude measurements
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

bRate = 230400
portNum = '/dev/tty.usbserial-DJ00DV99' # Differs for MAC AND PC
Fs = 10000 # Sampling freq in Hz
inputBufferSize = 10000 # 20 000 = 1 second buffer
bufferFillTime = inputBufferSize/20000.0 # Time to fill a buffer in seconds
ser = serial.Serial(port=portNum, baudrate=bRate)
ser.timeout = inputBufferSize/20000.0 

# Setup Plot
plotFlag = True
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
plt.ion()
fig.show()
fig.canvas.draw()

loopCount = 0
t = []
dataActual = [] # Store streaming data - NOT NEEDED FOR FINAL IMPLEMENTATION AS ONLY NEED DATA FROM CURRENT BUFFER

try:
    while True:
        data = read_arduino(ser, inputBufferSize)  # Read in data from current buffer
        dataTemp = process_data(data) # Temporarily store data from current buffer
        dataActual = np.append(dataTemp, dataActual)
        t = np.double((loopCount +1)*inputBufferSize/20000.0 * np.linspace(0,1,len(dataActual)))
        loopCount += 1
        ax1.clear()
        ax1.set_xlim(0, 5)
        plt.xlabel('time (s)')
        ax1.plot(t, dataActual)
        fig.canvas.draw()
        plt.draw()
        plt.pause(0.001)
except KeyboardInterrupt:
    pass


# SAVE TO WAVE FILE
fileName = 'rawData.txt'
np.savetxt(fileName, np.c_[t, dataActual])



if ser.read():
    ser.flushInput()
    ser.flushOutput()
    ser.close()
