from typing import List, Optional

import time
from xml.dom.minidom import getDOMImplementation
from serial import Serial
import numpy as np
import pandas as pd

from BrainboxStream import BrainboxStream
from Classify import Classify
import filters
import filters.downsample


brainbox_stream = BrainboxStream()
classify = Classify()

while True:
    data = brainbox_stream.read()
    if data is None:
        print("No amplitude data")
        continue
    #print(len(data), data)

    # Filter if needed
    # data = filters.spiker_filter.LP_Filter(data)
    # print(len(data), data)

    # Downsample
    data = filters.downsample.mean(data, factor=100)
    print(len(data), data[:10])

    # Classify


    # Send signal to UI if needed

