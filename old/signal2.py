import os, signal, time, sys

"""
SIGUSR1 - LEFT
SIGUSR2 - RIGHT
SIGWINCH - SELECT
"""
def send_signal(pid):
    os.kill(pid, signal.SIGUSR1)
    time.sleep(2)
    os.kill(pid, signal.SIGUSR2)
    time.sleep(2)
    os.kill(pid, signal.SIGWINCH)
    time.sleep(2)

def main(pid):
    while True:
        print("sending signal to pid " + str(pid))
        send_signal(pid)

if __name__ == '__main__':
    main(int(sys.argv[1]))
