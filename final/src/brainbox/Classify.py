import tensorflow as tf
from tensorflow import keras

class Classify:
    def __init__(self):
        new_model = tf.keras.models.load_model('./brainbox/models/model_1.h5')
        new_model.summary()
    pass

test = Classify()