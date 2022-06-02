import config

from data_load import load_sample_data, load_event_data, downsample, get_time_interval, plot_samples_events_individual
from data_merge import merge_samples_events, plot_merge_df
from data_transform import get_event_sequences

import numpy as np
import pandas as pd
import wave
import math
import matplotlib.pyplot as plt
import tensorflow as tf


def get_ml_data(
    file_paths: list[str],
    event_length: float = 4,
    event_start: float = -0.25,
    event_end: float = 0.25,
    downsample_rate: int = 100,
    shuffle_data:bool = True,

):
    """
    Returns a data and labels as loaded from multiple files.
    """
    print(f"Loading ML data from {len(file_paths)} files")
    data = []
    labels = []

    for file_path in file_paths:

        samples_df = load_sample_data(file_path)
        samples_df = downsample(samples_df, n=downsample_rate)
        events_df = load_event_data(file_path)
        # events_df["time_sec"] -= 3.5

        # print(samples_df)
        # print(events_df)

        merge_df = merge_samples_events(samples_df, events_df, event_start, event_end)

        # time_start = 30
        # time_end = 60
        # merge_df = get_time_interval(merge_df, time_start, time_end)
        # print(merge_df)

        # print(merge_df)
        # plot_merge_df(merge_df)

        # Get sequence data for ML
        seq_data, seq_labels = get_event_sequences(merge_df, event_length=event_length)
        # print(seq_data.shape, seq_data)
        # print(seq_labels.shape, seq_labels)

        data.append(seq_data)
        labels.append(seq_labels)

    data = np.concatenate(data)
    # print(data.shape, data)

    labels = np.concatenate(labels)
    labels[labels == -1] = 0 # Replace -1 (no event) with 0
    # print(labels.shape, labels)

    # Random arrange data
    if shuffle_data:
        print("Shuffling data sequences and labels")
        new_idx = np.random.permutation(len(data))
        data = data[new_idx]
        labels = labels[new_idx]

    print(f"Combined {len(file_paths)} files into {data.shape[0]} sequences of size {data.shape[1]}")

    return (data, labels)
