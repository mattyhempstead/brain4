import numpy as np
import pandas as pd
import wave
import math
import matplotlib.pyplot as plt

import config


def load_sample_data_wave(file_path:str):
    """ Read a brainbox wave file into a data frame """

    obj = wave.open(f'{file_path}.wav')

    print(obj)

    # Sample rate (brainbox looks to be 10k samples/sec)
    print(f"Sample rate: {obj.getframerate()} samples/sec")

    # Bytes per sample (brainbox is 2 bytes)
    print(f"Sample size: {obj.getsampwidth()} bytes")

    # Number of channels (brainbox gives 1)
    print(f"No. channels: {obj.getnchannels()}")

    # print(obj.getparams())

    # Read samples as int16 numpy array
    wav_frames = obj.readframes(nframes=2**32)
    ys = np.frombuffer(wav_frames, dtype=np.int16)
    # print(len(ys))
    # print(ys)

    samples_df = pd.DataFrame({
        "time_sec": np.arange(len(ys)) / obj.getframerate(),
        "sample": ys,
    })
    # print(samples_df)

    return samples_df


def load_sample_data(file_path:str):
    samples_df = pd.read_csv(
        f"{file_path}.txt",
        names=["time_sec", "sample"],
        header=1,
        sep=" ",
    )
    return samples_df


def load_event_data(file_path:str):
    """ Reads brainbox event data into a data frame """

    events_df = pd.read_csv(
        f"{file_path}Key.txt",
        names=["event_id", "time_sec"],
        header=1,
        quotechar="'",
    )

    if 0 in np.array(events_df["event_id"]):
        raise Exception("None event found in event file?")

    # Filter away all events not in event_type_map
    events_df = events_df[events_df["event_id"].isin(config.EVENT_TYPE_MAP.keys())]

    events_df["event_type"] = events_df["event_id"].map(config.EVENT_TYPE_MAP)
    events_df["event_color"] = events_df["event_id"].map(config.EVENT_COLOUR_MAP)

    # print(events_df)
    return events_df



def get_time_interval(df:pd.DataFrame, time_start:float, time_end:float):
    """ Returns a time interval of the sample/event data using time_sec """
    df_int = df[(df["time_sec"] >= time_start) & (df["time_sec"] < time_end)]
    df_int = df_int.reset_index(drop=True)
    return df_int



def downsample(sample_df, n=100):
    """
    Downsamples the wave data (not events) to 1/nth of a second by taking mean sample over that period.
    """
    # Downsample to 1/100th of a second 
    time_sec_n = np.floor(n*sample_df["time_sec"]) / n

    sample_df_n = pd.DataFrame({
        "time_sec": list(sample_df.groupby(time_sec_n)["time_sec"].min()),
        "sample": list(sample_df.groupby(time_sec_n)["sample"].mean()),
    })

    return sample_df_n



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
    event_length:int=None
):
    """
    Plots a single type of event
    """

    events_df_ind = events_df[events_df["event_id"] == event_id]
    num = len(events_df_ind)

    plt.figure(figsize=(14, 5), dpi=80)

    i = 0
    for idx,row in events_df_ind.iterrows():
        samples_df_int = get_time_interval(
            samples_df,
            row["time_sec"],
            row["time_sec"] + event_length
        )

        if i%3 == 0:
            plt.figure(figsize=(14, 5), dpi=80)

        plt.subplot(1, 3, 1+i%3)
        plt.title(f"Event {i+1}/{num} with id={event_id} @ t={row['time_sec']}")
        plt.plot(
            samples_df_int["time_sec"],
            samples_df_int["sample"],
            color="black",
        )

        if i % 3 == 2 or i == num-1:
            plt.show()

        i += 1



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
