import neural_net as nn
import numpy as np


class Snek:
    def __init__(self):
        # Neural Network that will output the decisions.
        self.brain = nn.NeuralNetwork()
        # List of pieces of a snek.
        self.pieces = []
        # Boolean value that determines whether a snek is playing.
        self.alive = True
        # Boolean value that determines whether a snek ate this turn.
        self.just_ate = False
        # Points to be maximized.
        self.points = 0

        # Populate the list of pieces.
        self.pieces.append((int(np.random.uniform(low=2, high=97)), int(np.random.uniform(low=2, high=97))))

        # Pieces will always be in one orientation (horizontal or vertical).
        orientation = int(np.random.uniform(low=0, high=1))

        # Snek will always initially move towards the side with greater space.
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
        # If a snek moves out of bounds, it dies.
        if self.pieces[0][0] < 0 or self.pieces[0][0] > 99:
            self.alive = False
        if self.pieces[0][1] < 0 or self.pieces[0][1] > 99:
            self.alive = False

        # If a snek collides with its own body, it dies.
        if self.pieces[0] in self.pieces[1:]:
            self.alive = False

    def move(self, direction):
        # Check whether a given direction is valid.
        if direction not in list(range(0, 4)):
            print('Invalid direction.')

        # Each move gives the snek one point.
        self.points += 1

        # Save the last piece in case the snek just ate.
        last_piece = self.pieces[-1]

        # Snek moves in the direction specified in the input.
        if direction == 0:
            self.pieces = [(self.pieces[0][0], self.pieces[0][1] + 1)] + self.pieces[:-1]
        elif direction == 1:
            self.pieces = [(self.pieces[0][0], self.pieces[0][1] - 1)] + self.pieces[:-1]
        elif direction == 2:
            self.pieces = [(self.pieces[0][0] + 1, self.pieces[0][1])] + self.pieces[:-1]
        elif direction == 3:
            self.pieces = [(self.pieces[0][0] - 1, self.pieces[0][1])] + self.pieces[:-1]

        # If snek just ate, do not remove last piece.
        if self.just_ate:
            self.pieces.append(last_piece)
            self.just_ate = False

    def eat(self):
        # If snek eats, set just_ate to true and earn 500 points.
        self.just_ate = True
        self.points += 500

    def predict(self, food):
        # Build the target array. snek's head x and y, food's x and y, and whether there is a part of the snek's body
        # in each of the four directions.
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

        # Call brain's predict.
        return self.brain.predict(target)

    def update(self, other_sneks):
        # Update weights and biases in brain with other sneks' brains.
        other_brains = []
        for snek in other_sneks:
            other_brains.append(snek.brain)

        # Call brain's update weights function.
        self.brain.update_weights(other_brains)

    def reset(self):
        # Function to reset everything but the weights and biases of a snake after playing. Useful for parent sneks that
        # will survive to the next generation. Explanation for each is given at the constructor.

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

