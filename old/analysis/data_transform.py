import numpy as np
import pandas as pd
import wave
import math
import matplotlib.pyplot as plt

import config

from data_load import load_sample_data, load_event_data, downsample, get_time_interval
from data_merge import merge_samples_events



def get_event_sequences(merge_df, event_length:float):
    """
    Returns a list of each time series sequence labelled by the event.
    """
    print("Transforming data into individual sequences...")

    seqs = []
    labels = []

    stop_time = max(merge_df["time_sec"]) - event_length

    for idx,row in merge_df.iterrows():
        # Stop when we are close to end of wave file
        if row["time_sec"] >= stop_time:
            break

        label = row["event_id"]
        if label is None:
            label = -1
        labels.append(label)

        seq = get_time_interval(
            merge_df,
            time_start = row["time_sec"],
            time_end = row["time_sec"] + event_length,
        )

        seq = list(seq["sample"])
        seqs.append(seq)


    # Crop sequences so they are all the same length
    # A bit hacky
    seq_length = min(len(seq) for seq in seqs)
    seqs = [seq[:seq_length] for seq in seqs]

    seqs = np.array(seqs)
    labels = np.array(labels)

    # Give a std of 1 and mean of 0
    # Could make it so that the live streaming data also has this property based on a moving avg or smth?
    sample_mean = merge_df["sample"].mean()
    sample_std = merge_df["sample"].std()
    for i,seq in enumerate(seqs):
        seqs[i] = (seq - sample_mean) / sample_std

    print(f"Transformed {seqs.shape[0]} sequences of size {seqs.shape[1]}")

    # print(seqs)
    # print(seqs.shape)
    # print(labels)
    # print(labels.shape)

    return (seqs, labels)




if __name__ == '__main__':
    print("data_transform.py")


    FILE_PATH = "../data/DoubleBlinkLR_Alex"

    samples_df = load_sample_data(FILE_PATH)
    samples_df = downsample(samples_df, n=100)
    events_df = load_event_data(FILE_PATH)

    merge_df = merge_samples_events(samples_df, events_df)

    # time_start = 30
    # time_end = 60
    # merge_df = get_time_interval(merge_df, time_start, time_end)
    # print(merge_df)

    event_length = 3
    seq_data, seq_labels = get_event_sequences(merge_df, event_length=event_length)

    print(seq_data)
    print(seq_labels)




