import numpy as np
from keras.layers import Dense
from keras.models import Sequential

pred = np.array([[2, 2, 25, 30, 0, 0, 1, 0]])

model = Sequential()
model.add(Dense(5, activation='relu', input_shape=(8, )))
model.add(Dense(5, activation='relu'))
model.add(Dense(4, activation='sigmoid'))
model.compile(optimizer='adam', loss='categorical_crossentropy')

print('Prediction:', model.predict(pred))

for i in range(1000):
    '''
    new_weights = []
    new_weights.append(np.random.random_sample((8, 5)))
    new_weights.append(np.random.random_sample((5, )))
    new_weights.append(np.random.random_sample((5, 5)))
    new_weights.append(np.random.random_sample((5, )))
    new_weights.append(np.random.random_sample((5, 4)))
    new_weights.append(np.random.random_sample((4, )))
    '''
    new_weights = np.array(model.get_weights()) + 1e-3
    model.set_weights(np.array(new_weights))

    this_pred = model.predict(pred)
    print('Iteration %i:' % (i + 1))
    print('    Prediction:', this_pred)
