from turtle import color
from click import style
import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
import time
import matplotlib
from setting import *


class Classify:
    PLOT_PREDICTIONS = False

    def __init__(self):
    
        self.model = tf.keras.models.load_model('./brainbox/models/model_1.h5')
        self.model.summary()

        self.p_hist = [[], [], [], []]
        self.p_ehist = []

        self.counter = 0
        if Classify.PLOT_PREDICTIONS:
            self.fig = plt.figure(figsize=(15,5))
            self.fig_ehist = plt.figure(figsize=(15,5))
            self.ax= self.fig.add_subplot(1,1,1)
            self.ax_ehist= self.fig_ehist.add_subplot(1,1,1)

            plt.ion()
            self.fig.show()
            self.fig_ehist.show()
            self.fig.canvas.draw_idle()
            self.fig_ehist.canvas.draw_idle()
            plt.xlabel('time (s)')

    def plot_phist(self):
        self.counter += 1
        if self.counter % 1 == 0:
            self.ax.clear()
            self.ax.set_title('Live Probabilities')
            self.ax.set_ylim([0,1])
            self.ax.plot(self.p_hist[0], color='black')
            self.ax.plot(self.p_hist[1], color='red')
            self.ax.plot(self.p_hist[2], color='green')
            self.ax.plot(self.p_hist[3], color='blue')

    def plot_ehist(self):
        self.counter += 1
        if self.counter % 1 == 0:
            self.ax_ehist.clear()
            self.ax_ehist.set_title('Event Prediction History')
            self.ax_ehist.set_ylim([0,3])
            self.ax_ehist.plot(self.p_ehist, color='black')

    def predict(self, data):
        #print(data)
        data = np.array([data])
        p = self.model.predict(data)
        #print(p)
        p = tf.nn.softmax(p, axis=1)[0]

        for i in range(len(p)):
            self.p_hist[i].append(p[i])
            self.p_hist[i] = self.p_hist[i][-FPS*10:]
        # print(len(self.p_hist[0]))
    
        p_list = [f"{100*i:6.2f}" for i in list(np.array(p))]

        if Classify.PLOT_PREDICTIONS:
            self.plot_phist()
            self.plot_ehist()

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
        self.p_ehist.append(event_pred)
        self.p_ehist = self.p_ehist[-FPS*10:]
        print(event_pred)
        return event_pred

