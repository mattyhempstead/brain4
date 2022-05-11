import time
import datetime
import os

class KeyLogger:
    KEYLOG_PATH = "./data_collection/data/"

    def __init__(self, person:str, electrode_placement:int, brainbox_number:int):
        self.person = person
        self.electrode_placement = electrode_placement
        self.brainbox_number = brainbox_number


        os.makedirs(KeyLogger.KEYLOG_PATH, exist_ok=True)
        self.file = open(KeyLogger.KEYLOG_PATH + self.get_file_name(), "w")
        self.file.write("time_sec,action,action_name\n")


    def get_file_name(self):
        p = self.person.title()
        ep = str(self.electrode_placement)
        bn = str(self.brainbox_number)

        d = str(datetime.datetime.now())[:10]
        t = int(time.time())

        return f"KEYLOG_{d}_{p}_{bn}_{ep}_{t}.csv"


    def write(self, action:str, action_name:str=""):
        self.file.write(f"{time.time()},{action},{action_name}\n")
        self.file.flush()

    def close(self):        
        self.file.close()



