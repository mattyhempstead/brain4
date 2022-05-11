from turtle import color
from click import style
import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
import time
import matplotlib
matplotlib.use('Qt5agg')


class Classify:
    def __init__(self):
    
        new_model = tf.keras.models.load_model('./brainbox/models/model_1.h5')
        new_model.summary()
        self.new_model = new_model
        self.p_hist = [[], [], [], []]
        self.fig = plt.figure(figsize=(15,5))
        self.ax= self.fig.add_subplot(1,1,1)
        plt.ion()
        self.fig.show()
        self.fig.canvas.draw_idle()
        plt.xlabel('time (s)')
        self.counter = 0

    def predict(self, data):
        #print(data)
        data = np.array([data])
        p = self.new_model.predict(data)
        #print(p)
        p = tf.nn.softmax(p, axis=1)[0]

        for i in range(len(p)):
            self.p_hist[i].append(p[i])
            self.p_hist[i] = self.p_hist[i][-30*10:]
        print(len(self.p_hist[0]))
    
        p_list = [f"{100*i:6.2f}" for i in list(np.array(p))]
        self.counter += 1
        if self.counter % 1 == 0:
            self.ax.clear()
            self.ax.set_ylim([0,1])
            self.ax.plot(self.p_hist[0], color='black')
            self.ax.plot(self.p_hist[1], color='red')
            self.ax.plot(self.p_hist[2], color='green')
            self.ax.plot(self.p_hist[3], color='blue')
            #self.fig.canvas.draw_idle()  
            #plt.draw()
            #plt.pause(0.001)
        # plt.scatter(time.time(),p[1],color='green', s=10)
        # plt.pause(0.00001)
        # plt.scatter(time.time(),p[2],color='blue', s=10)
        # plt.pause(0.00001)
        # plt.scatter(time.time(),p[3],color='red', s=10)
        # plt.pause(0.00001)
    
        # plt.xlim([time.time()-10, time.time()])
        print(p_list)
        #print(list(np.array(p[0])))
        event_pred = np.argmax(p)
        print(event_pred)
        return event_pred

