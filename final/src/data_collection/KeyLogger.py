import time
import datetime
import os

class KeyLogger:
    KEYLOG_PATH = "./data_collection/data/events/"
    WAVE_PATH = "./data_collection/data/waves/"

    def __init__(
        self,
        person:str,
        electrode_placement:int,
        brainbox_number:int,
        start_time:int,
    ):
        self.person = person
        self.electrode_placement = electrode_placement
        self.brainbox_number = brainbox_number
        self.start_time = start_time


        os.makedirs(KeyLogger.KEYLOG_PATH, exist_ok=True)
        self.file = open(KeyLogger.KEYLOG_PATH + self.get_file_name(), "w")
        self.file.write("time_sec,action,action_name\n")

        os.makedirs(KeyLogger.WAVE_PATH, exist_ok=True)
        self.file_wave = open(KeyLogger.WAVE_PATH + self.get_file_name(), "w")
        self.file_wave.write("time_sec,sample\n")


    def get_file_name(self):
        p = self.person.title()
        ep = str(self.electrode_placement)
        bn = str(self.brainbox_number)

        d = str(datetime.datetime.now())[:10]
        t = self.start_time

        return f"DATA_{d}_{p}_{bn}_{ep}_{t}.csv"


    def write(self, action:str, action_name:str=""):
        self.file.write(f"{time.time()},{action},{action_name}\n")
        self.file.flush()

    def write_sample(self, sampleValues, fs):
        t = time.time()
        print(t, len(sampleValues))
        for i in range(len(sampleValues)):
            t_s = t - (1/fs) * (len(sampleValues)-1-i)
            self.file_wave.write(f"{t_s},{sampleValues[i]}\n")
        self.file_wave.flush()
        #print(sampleValues, fs)

    def close(self):        
        self.file.close()



