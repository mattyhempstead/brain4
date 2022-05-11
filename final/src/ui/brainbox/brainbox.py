from typing import List, Optional

import time
from xml.dom.minidom import getDOMImplementation
from serial import Serial
import numpy as np
import pandas as pd
import signal
import random

from brainbox.BrainboxStream import BrainboxStream
from brainbox.Classify import Classify
from brainbox.filters import spiker_filter, downsample

from setting import *

loop_time = time.time()


brainbox_stream = BrainboxStream()
classify = Classify()

def brainbox_loop():
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
    #print(len(data), data[:10])

    # Classify
    classify.predict(data)
    
    # # Send signal to UI if needed
    # if random.random() < 0.05:
    #     pygame.event.post(LEFT_EVENT)
    # elif random.random() < 0.05:
    #     pygame.event.post(RIGHT_EVENT)
    # elif random.random() < 0.05:
    #     pygame.event.post(SELECT_EVENT)

