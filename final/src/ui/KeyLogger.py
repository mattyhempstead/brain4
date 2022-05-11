import time

class KeyLogger:
    KEYLOG_PATH = "../../data/keylog.txt"

    def __init__(self):
        self.file = open(KeyLogger.KEYLOG_PATH, "w")

        self.file.write("time_sec,action\n")

    def write(self, action:str):
        self.file.write(f"{time.time()},{action}\n")

    def close(self):        
        self.file.close()
