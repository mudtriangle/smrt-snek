import numpy as np
from keras.layers import Dense
from keras.models import Sequential


class NeuralNetwork:
    def __init__(self):
        self.model = Sequential()
        self.model.add(Dense(5, activation='relu', input_shape=(8,)))
        self.model.add(Dense(5, activation='relu'))
        self.model.add(Dense(4, activation='sigmoid'))
        self.model.compile(optimizer='adam', loss='categorical_crossentropy')

    def update_weights(self, other_nn):
        this_weights = np.array(self.model.get_weights())
        other_weights = np.array(other_nn.model.get_weights())

        new_weights = (this_weights + other_weights) / 2.0

        self.model.set_weights(new_weights)

    def predict(self, arr):
        return self.model.predict(arr)


pred = np.array([[2, 2, 25, 30, 0, 0, 1, 0]])
nn = NeuralNetwork()
for i in range(1000):
    nn.update_weights(NeuralNetwork())

    this_pred = nn.predict(pred)
    print('Iteration %i:' % (i + 1))
    print('    Prediction:', this_pred)

