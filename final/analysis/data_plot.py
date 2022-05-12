import numpy as np
import pandas as pd
import wave
import math
import matplotlib.pyplot as plt


def plot_samples_events(samples_df, events_df, event_length:int=None):
    """
    Plots events alongside samples.

    event_length determines the length of the shaded region following the event marker.
    event_length=None will not shade a region after the marker.
    """
    plt.plot(
        samples_df["time_sec"],
        samples_df["sample"],
        color="black",
        # label="Sample Data"
    )

    for idx,row in events_df.iterrows():
        # Shaded region
        if event_length is not None:
            plt.axvspan(
                xmin = row["time_sec"],
                xmax = row["time_sec"] + event_length,
                color=row["event_color"],
                label=row["event_type"],
                alpha=0.2
            )

        # Line at event marker
        plt.axvline(
            x = row["time_sec"],
            color=row["event_color"],
        )

    plt.legend()
    plt.show()


def plot_samples_events_individual(
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

    events_df_ind = events_df[events_df["event_id"] == event_id]
    num = len(events_df_ind)

    plt.figure(figsize=(14, 3), dpi=80)

    i = 0
    for idx,row in events_df_ind.iterrows():
        sample_idx = samples_df[samples_df["time_sec"] >= row["time_sec"]].index[0]
        sample_idx += event_sample_offset
        # print(row["time_sec"], sample_idx)

        samples_df_int = samples_df[sample_idx:sample_idx+event_sample_count]

        if i%3 == 0:
            plt.figure(figsize=(14, 3), dpi=80)

        plt.subplot(1, 3, 1+i%3)
        plt.title(f"Event {i+1}/{num} id={event_id} @ t={row['time_sec']}")
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

        if i % 3 == 2 or i == num-1:
            plt.show()

        i += 1


