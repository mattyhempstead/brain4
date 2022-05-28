# import config

from data_load import load_sample_data, load_event_data, downsample
from data_merge import merge_samples_events
from data_transform import get_event_sequences

import numpy as np
import pandas as pd
import wave
import math
import matplotlib.pyplot as plt
import tensorflow as tf


def get_ml_data(
    events_path: str,
    samples_path: str,
    file_names: list,

    event_id_map: dict,
    event_color_map: dict,

    event_sample_count: int = 300,
    event_start: float = -0.25,
    event_end: float = 0.25,

    downsample_rate: int = 100,

    shuffle_data:bool = True,
    filter_data: bool = True,

    debug:bool = False,
):
    """
    Returns a data and labels as loaded from multiple files.
    """
    print(f"Loading ML data from {len(file_names)} files\n")
    data = []
    labels = []

    for file_name in file_names:
        if debug: print(f"Loading sample file {file_name}")
        samples_df = load_sample_data(samples_path + file_name)
        if debug: print(f"Loaded {len(samples_df)} samples")
        if debug: print(f"Downsampling @ n={downsample_rate}")
        samples_df = downsample(samples_df, n=downsample_rate)
        if debug: print(f"Downsampled to {len(samples_df)} samples")

        if debug: print(f"Loading event file {file_name}")
        events_df = load_event_data(
            file_path = events_path + file_name,
            event_id_map = event_id_map,
            event_color_map = event_color_map,
        )
        if debug: print(f"Loaded {len(events_df)} events")
        

        if debug: print(f"Merging samples and events")
        merge_df = merge_samples_events(
            samples_df, events_df, event_start, event_end,
            event_id_map = event_id_map,
            event_color_map = event_color_map,
        )
        if debug: print("Merge complete")

        # time_start = 30
        # time_end = 60
        # merge_df = get_time_interval(merge_df, time_start, time_end)
        # print(merge_df)

        # print(merge_df)
        # plot_merge_df(merge_df)

        # Get sequence data for ML
        seq_data, seq_labels = get_event_sequences(
            merge_df,
            event_sample_count=event_sample_count,
            filter_data=filter_data,
        )
        # print(seq_data.shape, seq_data)
        # print(seq_labels.shape, seq_labels)
        
        data.append(seq_data)
        labels.append(seq_labels)

        print("")

    data = np.concatenate(data)
    # print(data.shape, data)

    labels = np.concatenate(labels)
    # print(labels.shape, labels)

    # Random arrange data
    if shuffle_data:
        if debug: print("Shuffling data sequences and labels")
        new_idx = np.random.permutation(len(data))
        data = data[new_idx]
        labels = labels[new_idx]

    print(f"Combined {len(file_names)} files into {data.shape[0]} sequences of size {data.shape[1]}")

    return (data, labels)
