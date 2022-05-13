from socket import timeout
from typing import List, Optional

from setting import *

import time
from xml.dom.minidom import getDOMImplementation
from serial import Serial
import numpy as np
import pandas as pd
import glob
import serial

# Check for polarity upon launching - left = trough followed by peak and vice versa for right


class BrainboxStream:

    FAKE_ARDUINO = False

    def __init__(self):
        self.time = time.perf_counter()

        # i think stream values per second?
        self.Fs = 10000.0
        
        self.baudrate = 230400
        self.port_num = self.get_port()

        # Buffer to read from brainbox
        self.window_buffer_time = 0.2
        self.window_buffer_size = int(self.window_buffer_time * self.Fs)
        self.window_buffer = []

        # Total buffer maintained over time
        self.full_buffer_time = 2
        self.full_buffer_size = int(self.full_buffer_time * self.Fs)
        self.full_buffer = []

        # Buffer of all data
        self.temp_buffer_time = 60
        self.temp_buffer_size = int(self.temp_buffer_time * self.Fs)
        self.tempBuffer = []

        self.serial:Serial = self.get_stream()


    def get_port(self) -> str:
        if BrainboxStream.FAKE_ARDUINO:
            return None

        # Check for serial name (MAC specific)
        if glob.glob('/dev/tty.usbserial*'):
            serialName = glob.glob('/dev/tty.usbserial*')
        elif glob.glob('/dev/tty.usbmodem*'):
            serialName = glob.glob('/dev/tty.usbmodem*')
        else:
            raise Exception('SERIAL NOT DETECTED')
        return serialName[0]

    def get_stream(self):
        if BrainboxStream.FAKE_ARDUINO:
            return None

        return Serial(
            port=self.port_num,
            baudrate=self.baudrate,
            timeout = 0,
            #parity= serial.PARITY_NONE
        )

    def read_arduino(self):
        """ Read unprocessed data from spikerBox """
        data = self.serial.read(self.window_buffer_size)  # blocking
        out = np.array([int(i) for i in data])
        return out

    def read_amplitudes(self):
        """ Read amplitude measurements from spikerBox """
        if BrainboxStream.FAKE_ARDUINO:
            # Return a random stream
            if np.random.random() < 0.05:
                return None
            else:
                return np.random.normal(size=np.random.randint(1,2*self.Fs/FPS))

        raw_data = self.read_arduino()
        if raw_data is None:
            return None

        # Convert spikerBox data to list of amplitude measurements
        amp_data = []
        i = 1
        while i < len(raw_data) - 1:
            if raw_data[i] > 127:
                intOut = (np.bitwise_and(raw_data[i], 127)) * 128
                i += 1
                intOut += raw_data[i]
                amp_data = np.append(amp_data, intOut)
            i += 1
        #print('Raw Data: ', len(raw_data), 'Amp Data: ', len(amp_data))
        return amp_data

    def read(self) -> Optional[np.array]:
        """ Read next arduino stream input and return processed data if ready """
        amp_data = self.read_amplitudes()
        if amp_data is None:
            # print("Arduino buffer not full")
            return None

        #print(amp_data)

        # Add to full_buffer and limit max length
        self.full_buffer = np.append(self.full_buffer, amp_data)
        self.tempBuffer = np.append(self.tempBuffer, amp_data)
        #print(self.full_buffer)

        self.full_buffer = self.full_buffer[-self.full_buffer_size:]
        #print(self.full_buffer_size, len(self.full_buffer))

        self.tempBuffer = self.tempBuffer[-self.temp_buffer_size:]
        # print('Temp Buffer size: ', len(self.tempBuffer))

        # Return None if not ready for full sequence
        if len(self.full_buffer) < self.full_buffer_size:
            print("Building full_buffer", len(self.full_buffer))
            return None

        self.print_time()

        return (self.full_buffer - self.tempBuffer.mean())/self.tempBuffer.std() 

    def print_time(self):
        t = time.perf_counter() - self.time
        self.time = time.perf_counter()
        print(f"Read time: {100*t:5.2f}ms")
