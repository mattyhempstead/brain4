import numpy as np
import pandas as pd
import wave
import math
import matplotlib.pyplot as plt

from scipy import signal
import numpy as np

# Butterworth filter
def LP_Filter(rawData, order:int=5, cutOff:int=7, Fs:int=10000):
    """
    cutOff in Hz
    """
    b, a = signal.butter(order, Wn=cutOff/(Fs/2)) 
    # Zero Phase double filter
    filteredSignal = signal.filtfilt(b, a, rawData)
    return filteredSignal



def get_event_sequences(merge_df, event_sample_count:int, filter_data:bool):
    """
    Returns a list of each time series sequence labelled by the event.
    """
    print("Transforming data into individual sequences...")

    seqs = []
    labels = []

    # plt.plot(merge_df["time_sec"], merge_df["sample"])
    # plt.show()

    # # Apply filters before we do the normalisation
    # # Not sure how to apply this to a data stream?
    # # When applied to a single 2 second sample it seems to stuff it up
    # if filter_data:
    #     merge_df["sample"] = LP_Filter(merge_df["sample"])

    # print(merge_df["sample"])
    # # plt.xlim(0,30)
    # plt.plot(merge_df["time_sec"], merge_df["sample"])
    # plt.show()


    for idx,row in merge_df[:-event_sample_count].iterrows():
        label = row["event_id"]
        if label is None:
            label = -1
        labels.append(label)

        seq = list(merge_df["sample"][idx:idx+event_sample_count])
        seqs.append(seq)

    seqs = np.array(seqs)
    labels = np.array(labels)

    # Apply filters before we do the normalisation
    # One reason is that mains 50Hz will increase std for that sample
    if filter_data:
        for i,seq in enumerate(seqs):
            seqs[i] = LP_Filter(seq, cutOff=7, Fs=100) # Account for downsampling

    # Give a std of 1 and mean of 0
    # Could make it so that the live streaming data also has this property based on a moving avg or smth?
    # sample_mean = merge_df["sample"].mean()
    # sample_std = merge_df["sample"].std()
    # for i,seq in enumerate(seqs):
    #     seqs[i] = (seq - sample_mean) / sample_std

    # Normalise relative to the 2 second interval
    # Note that this method will scale non-actions to have large magnitudes
    for i,seq in enumerate(seqs):
        seqs[i] = (seq - seq.mean()) / seq.std()

    print(f"Transformed into {seqs.shape[0]} sequences of size {seqs.shape[1]}")

    # print(seqs)
    # print(seqs.shape)
    # print(labels)
    # print(labels.shape)

    return (seqs, labels)




# if __name__ == '__main__':
#     print("data_transform.py")


#     FILE_PATH = "../data/DoubleBlinkLR_Alex"

#     samples_df = load_sample_data(FILE_PATH)
#     samples_df = downsample(samples_df, n=100)
#     events_df = load_event_data(FILE_PATH)

#     merge_df = merge_samples_events(samples_df, events_df)

#     # time_start = 30
#     # time_end = 60
#     # merge_df = get_time_interval(merge_df, time_start, time_end)
#     # print(merge_df)

#     event_length = 3
#     seq_data, seq_labels = get_event_sequences(merge_df, event_length=event_length)

#     print(seq_data)
#     print(seq_labels)




