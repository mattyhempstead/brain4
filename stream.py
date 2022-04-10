import serial
import numpy as np
import matplotlib.pyplot as plt


# Read unprocessed data from the spikerBox
def read_arduino(ser, inputBuffersize):
    data = ser.read(inputBuffersize)
    out = [(int(data[i])) for i in range(0,len(data))]
    return out

# Convert spikerBox data to a list of amplitude measurements
def process_data(dataIn):
    rawData = np.array(dataIn)
    processedData = []
    i = 1
    while i < len(rawData) - 1:
        if rawData[i] > 127:
            # Found beginning of frame. Extract one sample from two bytes
            intOut = (np.bitwise_and(rawData[i],127)) * 128
            i += 1
            intOut += rawData[i]
            processedData = np.append(processedData, intOut)
        i += 1
    return processedData

################################# Set SpikerBox parameters ###############################################
bRate = 230400
portNum = '/dev/tty.usbserial-DJ00E2W2' #WILL DIFFER BETWEEN MAC AND PC
inputBufferSize = 20000 # NOTE 20000 = 1 second buffer
ser = serial.Serial(port=portNum, baudrate=bRate) # Setup communication channel
ser.timeout = inputBufferSize/20000.0
ser.set_buffer_size(rx_size=inputBufferSize)
#######################################################################################################

# Time-limited data streaming - can adjust to make indefinite
totalTime = 20 # Total Streaming time in seconds
plotWindowTime = 10 # Total time plotted in window in seconds
numLoops = 20000.0/inputBufferSize*totalTime #Number of buffer loops in entire streaming period
tAcquire = inputBufferSize/20000.0 # Period of time that data is acquired for to fill buffer (in seconds)
plotWindowLoops = plotWindowTime/tAcquire # Number of loops required to fill the entire plot window

# Setup the plot window
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
plt.ion()
fig.show()
fig.canvas.draw()
########################################################################################################

# Initiate data collection loops and plot data for each filled buffer
dataPlot = []
for k in range(0, int(numLoops)):
    data = read_arduino(ser, inputBufferSize) # Read in the data from the current buffer
    dataTemp = process_data(data) #Store the data in the current buffer
    if k <= plotWindowLoops:
        # If the current loops are to be plotted in the window
        dataPlot = np.append(dataTemp, dataPlot)
        t = (min(k+1, plotWindowLoops))*inputBufferSize/20000.0*np.linspace(0,1,(dataPlot).size)
    else:
        # If data is just being recorded (not plotted), continue to add to the array
        dataPlot = np.roll(dataPlot, len(dataTemp)) # Designate space to the start of the array for new data
        dataPlot[0:len(dataTemp)] = dataTemp # Fill new space with data
    t = (min(k+1, plotWindowLoops))*inputBufferSize/20000.0*np.linspace(0,1,(dataPlot).size)

    # Plot data
    ax1.clear()
    ax1.set_xlim(0, plotWindowTime)
    plt.xlabel('time [s]')
    ax1.plot(t, dataPlot)
    fig.canvas.draw()
    plt.show()

##################################################################################################################

# SAVE DATA FROM STREAMING SESSION
fileName = 'stream.txt'
np.savetxt(fileName, np.c_[t, np.real(dataPlot)])


# Close serial port if necessary
if ser.read():
    ser.flushInput()
    ser.flushOutput()
    ser.close()











