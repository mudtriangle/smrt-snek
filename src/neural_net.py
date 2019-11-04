import numpy as np
from keras.layers import Dense
from keras.models import Sequential


class NeuralNetwork:
    def __init__(self):
        self.model = Sequential()
        self.model.add(Dense(120, activation='relu', input_shape=(8,)))
        self.model.add(Dense(120, activation='relu'))
        self.model.add(Dense(4, activation='sigmoid'))
        self.model.compile(optimizer='adam', loss='categorical_crossentropy')

    def update_weights(self, other_nns):
        new_weights = np.array(self.model.get_weights())

        relevance = 99 / len(other_nns)
        for other_nn in other_nns:
            other_weights = np.array(other_nn.model.get_weights())
            new_weights += other_weights * relevance

        new_weights = new_weights / 100

        self.model.set_weights(new_weights)

    def predict(self, arr):
        return self.model.predict(arr)
