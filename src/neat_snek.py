import numpy as np


class Snek:
    def __init__(self, net):
        # Neural Network that will output the decisions.
        self.brain = net

        # List of starting pieces of a snek.
        self.pieces = [(0, 2), (0, 1), (0, 0)]

        # Boolean value that determines whether a snek is playing.
        self.alive = True

        # Boolean value that determines whether a snek ate this turn.
        self.just_ate = False

        # Points to be maximized.
        self.points = 0

        # Prevents the snek to go too long without eating.
        self.hunger = 0

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

        # Each move gives the snek one point and one hunger.
        self.points += 1
        self.hunger += 1

        if self.hunger >= 200:
            self.alive = False

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
        self.hunger = 0

    def predict(self, food):
        # Build the target array. snek's head x and y, food's x and y, and whether there is a part of the snek's body
        # in each of the four directions.
        target = np.array([self.pieces[0][0], self.pieces[0][1], food[0], food[1], 0, 0, 0, 0])

        for piece in self.pieces[1:]:
            if piece[0] == self.pieces[0][0] and piece[1] > self.pieces[0][1]:
                target[4] = 1
            elif piece[0] == self.pieces[0][0] and piece[1] < self.pieces[0][1]:
                target[5] = 1
            elif piece[1] == self.pieces[0][1] and piece[0] < self.pieces[0][0]:
                target[6] = 1
            elif piece[1] == self.pieces[0][1] and piece[0] > self.pieces[0][0]:
                target[7] = 1

        # Call brain's predict.
        return self.brain.activate(target)
