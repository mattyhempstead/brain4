from pynput.keyboard import Key, Listener
import time
import numpy as np
import keyboard

keyPress = []
timePress = []
startFlag = False

def on_press(key):
    if key == Key.esc:
        return False
    print(key)
    keyPress.append(key)
    timePress.append(np.round(time.time()-startTime, 4))

print('Press s to start logging keypresses...')
if keyboard.read_key() == 's':
    startTime = time.time()
    with Listener(on_press=on_press) as listener:
        listener.join()

keyPressData = np.column_stack([keyPress, timePress])
fileName = 'keyPress.txt'
np.savetxt(fileName, keyPressData, fmt=['%s,', '%1.4f'])
