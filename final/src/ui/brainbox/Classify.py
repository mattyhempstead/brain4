from this import d
import tensorflow as tf
from tensorflow import keras
import numpy as np

class Classify:
    def __init__(self):
        new_model = tf.keras.models.load_model('./brainbox/models/model_1.h5')
        new_model.summary()
        self.new_model = new_model
    def predict(self, data):
        data = (data - data.mean())/data.std()
        #print(data)
        data = np.array([data])
        p = self.new_model.predict(data)
        #print(p)
        p = tf.nn.softmax(p, axis=1)
        print(list(np.array(p[0])))
        event_pred = np.argmax(p, axis=1)
        print(event_pred)
        return event_pred[0]

