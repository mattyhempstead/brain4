
import serial 
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt


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

# Set SpikerBox Parameters

bRate = 230400
portNum = '/dev/tty.usbserial-DJ00DV99' # Differs for MAC AND PC
Fs = 10000 # Sampling freq in Hz
inputBufferSize = 10000 # 20 000 = 1 second buffer
bufferFillTime = inputBufferSize/20000.0 # Time to fill a buffer in seconds
ser = serial.Serial(port=portNum, baudrate=bRate)
ser.timeout = inputBufferSize/20000.0 
# ser.set_buffer_size(rx_size=inputBufferSize) LINE NOT REQUIRED ON MAC

# Setup Calibration Phase
calibrationTime = 10 # Seconds
calibrationLoops = calibrationTime/bufferFillTime


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
calibrationArray = [] # Store calibration data

# Start Stream

try:
    while True:
        data = read_arduino(ser, inputBufferSize)  # Read in data from current buffer
        dataTemp = process_data(data) # Temporarily store data from current buffer
        if len(dataTemp) > 0:
            dataNorm = dataTemp
            n = len(dataTemp)
            dF = Fs/n  # Freq step
            start = -Fs/2
            end = Fs/2
            f = np.transpose(np.arange(start, end, dF))
            lowerFreqCutoff = 1 # Hz
            HpFilter = ((abs(f) > lowerFreqCutoff))
            spectrum = (np.fft.fftshift(np.fft.fft(dataNorm)))/n
            spectrum = np.multiply(HpFilter, spectrum)
            fftFiltered = np.abs(np.fft.ifft(np.fft.ifftshift(spectrum))*n)
            order = 5 # Butterworth filter order
            cutOffFreq = 10 # Hz
            normalizedCutoff = cutOffFreq/(Fs/2)
            b, a = signal.butter(order, Wn=normalizedCutoff)
            dataFiltered = signal.filtfilt(b,a, fftFiltered) # Butterworth filter
            if loopCount <= calibrationLoops:
                # CALIBRATION PHASE
                calibrationArray = np.append(dataFiltered, calibrationArray)
                calibrationT = np.double((loopCount+1)*inputBufferSize/20000.0 * np.linspace(0, 1, len(calibrationArray)))
                if plotFlag == True:
                    ax1.clear()
                    ax1.set_xlim(0, calibrationTime)
                    plt.xlabel('time (s)')
                    ax1.plot(calibrationT, calibrationArray)
                    fig.canvas.draw()
                    plt.draw()
                    plt.pause(0.001)
            else:
                # STREAMING PHASE
                if loopCount == (calibrationLoops+1):
                    noise = np.mean(calibrationArray) # Calculate baseline for subtraction
                filteredSignal = dataFiltered - noise # Subtract baseline
                dataActual = np.append(filteredSignal, dataActual) # Save to array - MAY JUST NEED TO DIRECTLY OUTPUT FILTERED SIG IN FINAL VERSION
                t = np.double((loopCount-calibrationLoops)*inputBufferSize/20000.0 * np.linspace(0,1,len(dataActual)))    # Start actual streaming at t = 0
                if plotFlag == True:
                    ax1.clear()
                    ax1.set_xlim(0, calibrationTime)
                    plt.xlabel('time (s)')
                    ax1.plot(t, dataActual)
                    fig.canvas.draw()
                    plt.draw()
                    plt.pause(0.001)
            loopCount += 1
except KeyboardInterrupt:
    pass

if ser.read():
    ser.flushInput()
    ser.flushOutput()
    ser.close()

