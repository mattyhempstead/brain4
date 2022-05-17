from typing import List, Optional
from serial import Serial
import numpy as np
import pandas as pd
import time
import signal
import random
import matplotlib.pyplot as plt

from brainbox.BrainboxStream import BrainboxStream
from brainbox.Classify import Classify
from brainbox.filters import spiker_filter, downsample

from setting import *



loop_time = time.time()
event_time = time.time()

brainbox_stream = BrainboxStream()
classify = Classify()

def brainbox_loop():
    print('Test')
    global loop_time

    t = time.time()
    #print(f"Loop {t:.3f} {1000*(t-loop_time):.2f}ms")
    loop_time = t


    data = brainbox_stream.read()
    if data is None:
        print("No amplitude data")
        return 
    #print(len(data), data)

    # # Filter if needed
    # # data = filters.spiker_filter.LP_Filter(data)
    # # print(len(data), data)

    # # Downsample
    data = downsample.mean(data, factor=100)
    print(len(data), data[:3])

    # Classify
    pred = classify.predict(data)

    # print(pred, len(data))
    # input()


    global event_time

    if time.time() < event_time:
        pred = 0
    
    if pred != 0:
        event_time = time.time() + 1
        print(pred, event_time)

    # Send signal to UI if needed
    if pred == 1:
        pygame.event.post(LEFT_EVENT)
    elif pred == 2:
        pygame.event.post(RIGHT_EVENT)
    elif pred == 3:
        pygame.event.post(SELECT_EVENT)

