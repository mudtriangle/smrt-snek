import neural_net as nn
import numpy as np


class Snek:
    def __init__(self):
        self.brain = nn.NeuralNetwork()
        self.pieces = []
        self.alive = True
        self.just_ate = False
        self.points = 0

        self.pieces.append((int(np.random.uniform(low=2, high=97)), int(np.random.uniform(low=2, high=97))))

        orientation = int(np.random.uniform(low=0, high=1))
        if orientation:
            if self.pieces[0][1] < 50:
                self.pieces.append((self.pieces[0][0], self.pieces[0][1] - 1))
                self.pieces.append((self.pieces[0][0], self.pieces[0][1] - 2))

            else:
                self.pieces.append((self.pieces[0][0], self.pieces[0][1] + 1))
                self.pieces.append((self.pieces[0][0], self.pieces[0][1] + 2))

        else:
            if self.pieces[0][0] < 50:
                self.pieces.append((self.pieces[0][0] - 1, self.pieces[0][1]))
                self.pieces.append((self.pieces[0][0] - 2, self.pieces[0][1]))

            else:
                self.pieces.append((self.pieces[0][0] + 1, self.pieces[0][1]))
                self.pieces.append((self.pieces[0][0] + 2, self.pieces[0][1]))

    def check_collision(self):
        if self.pieces[0][0] < 0 or self.pieces[0][0] > 99:
            self.alive = False
        if self.pieces[0][1] < 0 or self.pieces[0][1] > 99:
            self.alive = False

        if self.pieces[0] in self.pieces[1:]:
            self.alive = False

    def move(self, direction):
        if direction not in list(range(0, 4)):
            print('Invalid direction.')

        self.points += 1
        last_piece = self.pieces[-1]

        if direction == 0:
            self.pieces = [(self.pieces[0][0], self.pieces[0][1] + 1)] + self.pieces[:-1]
        elif direction == 1:
            self.pieces = [(self.pieces[0][0], self.pieces[0][1] - 1)] + self.pieces[:-1]
        elif direction == 2:
            self.pieces = [(self.pieces[0][0] + 1, self.pieces[0][1])] + self.pieces[:-1]
        elif direction == 3:
            self.pieces = [(self.pieces[0][0] - 1, self.pieces[0][1])] + self.pieces[:-1]

        if self.just_ate:
            self.pieces.append(last_piece)
            self.just_ate = False

    def eat(self):
        self.just_ate = True
        self.points += 500

    def predict(self, food):
        target = np.array([[self.pieces[0][0], self.pieces[0][1], food[0], food[1], 0, 0, 0, 0]])

        for piece in self.pieces[1:]:
            if piece[0] == self.pieces[0][0] and piece[1] > self.pieces[0][1]:
                target[0][4] = 1
            elif piece[0] == self.pieces[0][0] and piece[1] < self.pieces[0][1]:
                target[0][5] = 1
            elif piece[1] == self.pieces[0][1] and piece[0] < self.pieces[0][0]:
                target[0][6] = 1
            elif piece[1] == self.pieces[0][1] and piece[0] > self.pieces[0][0]:
                target[0][7] = 1

        return self.brain.predict(target)

    def update(self, other_sneks):
        other_brains = []
        for snek in other_sneks:
            other_brains.append(snek.brain)
        self.brain.update_weights(other_brains)

    def reset(self):
        self.pieces = []
        self.alive = True
        self.just_ate = False
        self.points = 0

        self.pieces.append((int(np.random.uniform(low=2, high=97)), int(np.random.uniform(low=2, high=97))))

        orientation = int(np.random.uniform(low=0, high=1))
        if orientation:
            if self.pieces[0][1] < 50:
                self.pieces.append((self.pieces[0][0], self.pieces[0][1] - 1))
                self.pieces.append((self.pieces[0][0], self.pieces[0][1] - 2))

            else:
                self.pieces.append((self.pieces[0][0], self.pieces[0][1] + 1))
                self.pieces.append((self.pieces[0][0], self.pieces[0][1] + 2))

        else:
            if self.pieces[0][0] < 50:
                self.pieces.append((self.pieces[0][0] - 1, self.pieces[0][1]))
                self.pieces.append((self.pieces[0][0] - 2, self.pieces[0][1]))

            else:
                self.pieces.append((self.pieces[0][0] + 1, self.pieces[0][1]))
                self.pieces.append((self.pieces[0][0] + 2, self.pieces[0][1]))

