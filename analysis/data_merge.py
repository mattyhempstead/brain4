import numpy as np
import pandas as pd
import wave
import math
import matplotlib.pyplot as plt

import config

from data_load import load_sample_data, load_event_data, downsample, get_time_interval



def merge_samples_events(samples_df, events_df, event_start:float = -0.25, event_end:float = 0.25):
    """
    Merges the sample and event dataframes.

    Events will be assigned to individual samples within a specified time range around the market.
    """
    # Add target classification event to each sample
    merge_df = samples_df.copy()

    # Default is None (no event)
    merge_df["event_id"] = None
    merge_df["event_type"] = None
    merge_df["event_color"] = None
    #print(sample_100_df)

    # Assign all events within range around their event marker
    for idx,row in events_df.iterrows():
        # Skip blinks for now
        # if row["event_type"] not in ["Left", "Right"]:
        #     continue

        event_interval = (merge_df["time_sec"] > (row["time_sec"] + event_start))
        event_interval &= (merge_df["time_sec"] < (row["time_sec"] + event_end))
        
        merge_df.loc[event_interval,"event_id"] = row["event_id"]
        merge_df.loc[event_interval,"event_type"] = row["event_type"]
        merge_df.loc[event_interval,"event_color"] = row["event_color"]

    return merge_df



def plot_merge_df(merge_df):

    plt.plot(
        merge_df["time_sec"],
        merge_df["sample"],
        color="black",
        # label="Sample Data"
    )

    sample_size = merge_df["time_sec"][1] - merge_df["time_sec"][0]
    for idx,row in merge_df.iterrows():
        if row["event_type"] is not None:
            plt.axvspan(
                xmin = row["time_sec"],
                xmax = row["time_sec"] + sample_size,
                color = row["event_color"],
                label = row["event_type"],
                alpha = 0.2
            )

    plt.show() 




if __name__ == "__main__":
    print("data_merge.py")

    FILE_PATH = "../data/DoubleBlinkLR_Alex"

    samples_df = load_sample_data(FILE_PATH)
    samples_df = downsample(samples_df, n=100)
    events_df = load_event_data(FILE_PATH)

    merge_df = merge_samples_events(samples_df, events_df)

    time_start = 30
    time_end = 60
    merge_df = get_time_interval(merge_df, time_start, time_end)

    print(merge_df)
    plot_merge_df(merge_df)
