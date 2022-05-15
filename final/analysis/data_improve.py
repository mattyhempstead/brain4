"""
Manually improve alignment issues in the data sources.


Events are plotted one at a time.

Entering a value will shift the line and bring the same plot up again.

"""
import numpy as np
import pandas as pd
import wave
import math
import matplotlib.pyplot as plt
import tensorflow as tf


from data_load import load_sample_data, load_event_data, downsample
from data_transform import LP_Filter

from data_plot import plot_samples_events_individual


BRAINBOX_SAMPLE_RATE = 10000

EVENT_ID_MAP = {
    None: 0,
    "L": 1,
    "R": 2,
    "S": 3,
}
EVENT_ID_LETTER_MAP = {EVENT_ID_MAP[i]:i for i in EVENT_ID_MAP}

EVENT_COLOR_MAP = {
    None: "black",
    "L": "red",
    "R": "blue",
    "S": "green",
}

EVENT_ID_NAME_MAP = {
    0: "Nothing",
    1: "Left Wink",
    2: "Right Wink",
    3: "Dbl Blink",
}

EVENTS_PATH = "../src/data_collection/data/events/"
SAMPLES_PATH = "../src/data_collection/data/waves/"

DOWNSAMPLE_RATE = 100

EVENT_LENGTH = 2 # length of a given event sequence in seconds
EVENT_SAMPLE_COUNT = int(EVENT_LENGTH * BRAINBOX_SAMPLE_RATE / DOWNSAMPLE_RATE) # size of event in samples

EVENT_START = -0.2
EVENT_START_OFFSET = int(EVENT_START * BRAINBOX_SAMPLE_RATE / DOWNSAMPLE_RATE)

EVENT_END = -0.1
EVENT_END_OFFSET = int(EVENT_END * BRAINBOX_SAMPLE_RATE / DOWNSAMPLE_RATE)

INPUT_SHAPE = (EVENT_SAMPLE_COUNT,)
OUTPUT_SHAPE = len(EVENT_ID_MAP)  # number of categories (including None)

FILE_NAMES = [
    "DATA_2022-05-12_Josh_0001_0_1652333343",
    "DATA_2022-05-12_Josh_0001_0_1652333800",
    "DATA_2022-05-12_Josh_0001_1_1652334198",
    "DATA_2022-05-12_Josh_0001_1_1652334982",
    "DATA_2022-05-12_Josh_0001_2_1652335485",
    "DATA_2022-05-12_Josh_0001_2_1652336009",
    "DATA_2022-05-13_Josh_0001_3_1652400625",
    "DATA_2022-05-13_Josh_0001_3_1652400939",
    "DATA_2022-05-13_Josh_0001_4_1652401267",
    "DATA_2022-05-13_Josh_0001_4_1652401740",
    "DATA_2022-05-13_Josh_0001_5_1652405337",
    "DATA_2022-05-13_Josh_0001_5_1652405637",
    "DATA_2022-05-13_Josh_0001_6_1652406023",
    "DATA_2022-05-13_Josh_0001_6_1652406202",
    "DATA_2022-05-13_Josh_0001_7_1652406589",
    "DATA_2022-05-13_Josh_0001_7_1652406788",
    "DATA_2022-05-13_Josh_0001_8_1652407331",
    "DATA_2022-05-13_Josh_0001_8_1652407508",
]

EVENT_ID = 1

PLOT_FILE_NAME = FILE_NAMES[16]
# PLOT_FILE_NAME = FILE_NAMES[15]
# PLOT_FILE_NAME = "DATA_test"

"""
1 - first trough
2 - first peak
3 - first trough
"""

def plot_file_events(
    samples_df, 
    events_df, 
    event_id:int,

    event_length:float,
    event_start:float,
    event_end:float,

    event_sample_count:int,
    event_sample_offset:int,
):
    """
    Plots a single type of event
    """
    print(events_df)
    print("")
    samples = samples_df["sample"]

    # Plot and query changes
    plt.ion()
    plt.figure(figsize=(14, 2), dpi=80)

    num = sum(events_df["event_id"] == event_id)

    stop = False
    i = 0
    for idx,row in events_df[events_df["event_id"] == event_id].iterrows():
        i += 1
        if stop:
            break

        while True:
            row = events_df.iloc[idx]

            sample_idx = samples_df[samples_df["time_sec"] >= row["time_sec"]].index[0]
            sample_idx += event_sample_offset
            # print(row["time_sec"], sample_idx)

            samples_df_int = samples_df[sample_idx:sample_idx+event_sample_count]

            plt.cla()
            plt.title(f"Event {i}/{num} id={event_id} @ t={row['time_sec']}")
            plt.plot(
                samples_df_int["time_sec"],
                (samples_df_int["sample"] - samples_df["sample"].mean()) / samples_df["sample"].std(),
                color="black",
            )

            plt.axvline(x=row["time_sec"], color="red")

            plt.axvline(x=row["time_sec"] + event_start, color="green")
            plt.axvline(x=row["time_sec"] + event_end, color="green")

            plt.axvline(x=row["time_sec"] + event_start + event_length, color="blue")
            plt.axvline(x=row["time_sec"] + event_end + event_length, color="blue")



            print("row timesec", row["time_sec"])

            sample_idx = samples_df[samples_df["time_sec"] >= row["time_sec"]].index[0]
            slope_event = int(math.copysign(1, samples_df["sample"][sample_idx+1] - samples_df["sample"][sample_idx]))
            print("slope_event", slope_event)

            # Get distance to local trough
            min_idx = sample_idx
            while True:
                # print("min idx", min_idx)
                # print(samples_df.iloc[min_idx]["time_sec"])
                # print(samples_df.iloc[left_min_idx]["sample"])
                # print(samples_df.iloc[left_min_idx-1]["time_sec"])
                # print(samples_df.iloc[left_min_idx]["time_sec"])
                # if min_idx == 0 or min_idx == len(samples_df)-1:
                #     break

                slope = int(math.copysign(1, samples_df["sample"][min_idx+1] - samples_df["sample"][min_idx]))
                if slope != slope_event:
                    break
                min_idx -= int(slope_event)

            min_dist = samples_df.iloc[min_idx]["time_sec"] - row["time_sec"]
            print("min dist", min_dist)


            # Get distance to local peak
            max_idx = sample_idx
            while True:
                # print("max idx", max_idx)
                # if max_idx == 0:
                #     break
                slope = int(math.copysign(1, samples_df["sample"][max_idx+1] - samples_df["sample"][max_idx]))
                if slope != slope_event:
                    break
                max_idx += int(slope_event)

                # if samples_df["sample"][max_idx] > samples_df["sample"][max_idx+1]:
                #     break
                # max_idx += 1

            max_dist = samples_df.iloc[max_idx]["time_sec"] - row["time_sec"]
            print("max dist", max_dist)


            move = input(f"Move event {i} by: ")
            
            if move == "":
                plt.pause(0.05)
                break
            elif move.lower() == "q":
                plt.pause(0.05)
                stop = True
                break
            elif move.lower() == "l":
                move = min_dist
            elif move.lower() == "u":
                move = max_dist

            try:
                move = float(move)
            except ValueError:
                move = 0
                print("Invalid move")

            events_df["time_sec"][idx] += move

            plt.pause(0.05)
    
    plt.close()

    print(events_df)

    # events_df["time_sec"] += min_time

    df = pd.DataFrame({
        "time_sec": events_df["time_sec"],
        "action": events_df["event_letter"],
        "action_name": events_df["event_name"],
    })
    df.to_csv(
        EVENTS_PATH + PLOT_FILE_NAME + ".csv",
        index = False,
        header = True,
    )



samples_df = load_sample_data(SAMPLES_PATH + PLOT_FILE_NAME)
samples_df["sample"] = LP_Filter(samples_df["sample"], cutOff=7)
samples_df = downsample(samples_df, n=DOWNSAMPLE_RATE)

events_df = load_event_data(
    file_path = EVENTS_PATH + PLOT_FILE_NAME,
    event_id_map = EVENT_ID_MAP,
    event_color_map = EVENT_COLOR_MAP,
)


plot_file_events(
    samples_df, events_df, 
    event_id = EVENT_ID,
    
    event_length = EVENT_LENGTH,
    event_start = EVENT_START,
    event_end = EVENT_END,
    
    event_sample_count = 600,
    event_sample_offset = -200,
)


