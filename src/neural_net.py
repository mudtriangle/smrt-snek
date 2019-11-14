import numpy as np
from keras.layers import Dense
from keras.models import Sequential

THRESHOLD = 1e-2


class NeuralNetwork:
    def __init__(self):
        # Basic structure of the neural network that will become the brain of a snek.
        self.model = Sequential()
        self.model.add(Dense(120, activation='relu', input_shape=(8,)))
        self.model.add(Dense(120, activation='relu'))
        self.model.add(Dense(4, activation='softmax'))
        self.model.compile(optimizer='adam', loss='categorical_crossentropy')

    def update_weights(self, other_nns, relevances):
        # Based on a list of other NeuralNetwork objects, update this NeuralNetwork's weights and biases.
        new_weights = np.array(self.model.get_weights())

        for i in range(len(new_weights)):
            for j in range(len(new_weights[i])):
                choice = np.random.uniform()
                if choice > THRESHOLD:
                    if len(other_nns) == 1:
                        parent = other_nns[0]
                    else:
                        parent = np.random.choice(other_nns, size=1, p=relevances)[0]

                    p_weights = parent.model.get_weights()
                    new_weights[i][j] = (np.array(p_weights)[i][j] * 99 + new_weights[i][j]) / 100

        # Save new weights and biases.
        self.model.set_weights(new_weights)

    def predict(self, arr):
        # Call keras' model's predict.
        return self.model.predict(arr)
