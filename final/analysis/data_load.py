import numpy as np
import pandas as pd
import wave
import math
import matplotlib.pyplot as plt



def load_sample_data(file_path:str):
    samples_df = pd.read_csv(
        f"{file_path}.csv",
    )

    # Sort because some samples are not written in order
    samples_df = samples_df.sort_values("time_sec", ascending=True)
    samples_df.reset_index(drop=True, inplace=True)

    return samples_df

def downsample(sample_df, n=100):
    """
    Downsamples the wave data (not events) to 1/nth of a second by taking mean sample over that period.
    """
    # Crop size to allow downsampling
    sample_df = sample_df[:len(sample_df) - (len(sample_df)%n)]
    
    return pd.DataFrame({
        "time_sec": np.min(np.array(sample_df["time_sec"]).reshape(-1,n), 1),
        "sample": np.mean(np.array(sample_df["sample"]).reshape(-1,n), 1),
    })

def downsample_arr(arr, n=100):
    # Crop size to allow downsampling
    arr = arr[:len(arr) - (len(arr)%n)]
    return np.mean(arr.reshape(-1,n), 1)

def load_event_data(file_path:str, event_id_map:dict, event_color_map:dict):
    """ Reads brainbox event data into a data frame """

    events_df = pd.read_csv(
        f"{file_path}.csv",
        names=["time_sec", "event_letter", "event_name"],
        header=0,
    )

    # # Filter away all events not in event_type_map
    # events_df = events_df[events_df["event_id"].isin(config.EVENT_TYPE_MAP.keys())]

    events_df["event_id"] = events_df["event_letter"].map(event_id_map)
    events_df["event_color"] = events_df["event_letter"].map(event_color_map)

    return events_df



def get_time_interval(df:pd.DataFrame, time_start:float, time_end:float):
    """ Returns a time interval of the sample/event data using time_sec """
    df_int = df[(df["time_sec"] >= time_start) & (df["time_sec"] < time_end)]
    df_int = df_int.reset_index(drop=True)
    return df_int







if __name__ == '__main__':
    print("data.py")

    FILE_PATH = "../data/DoubleBlinkLR_Alex"

    samples_df = load_sample_data(FILE_PATH)
    samples_df = downsample(samples_df, n=100)
    events_df = load_event_data(FILE_PATH)


    time_start = 30
    time_end = 60
    samples_df = get_time_interval(samples_df, time_start, time_end)
    events_df = get_time_interval(events_df, time_start, time_end)

    print("samples\n", samples_df)
    print("events\n", events_df)
    plot_samples_events(samples_df, events_df, event_length=3)
