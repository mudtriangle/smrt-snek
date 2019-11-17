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
        #  0,  1,  2,  3 are whether the food is in a direction UP, DOWN, LEFT, RIGHT.
        #  4,  5,  6,  7 are the distance from the head to the food, 0 if it is not in that direction.
        #  8,  9, 10, 11 are the distances from the head to the walls.
        # 12, 13, 14, 15 are whether there are parts of the snek in each of the four directions.
        # 16, 17, 18, 19 are the distance from the head to the parts of the snek, 0 if none in that direction.
        target = np.zeros(20)
        head = self.pieces[0]

        if food[0] < head[0]:
            target[0] = 1
            target[4] = head[0] - food[0]
        elif food[0] > head[0]:
            target[1] = 1
            target[5] = food[0] - head[0]

        if food[1] < head[1]:
            target[2] = 1
            target[6] = head[1] - food[1]
        elif food[1] > head[1]:
            target[3] = 1
            target[7] = food[1] - head[1]

        target[8] = head[0] + 1
        target[9] = 101 - target[8]
        target[10] = head[1] + 1
        target[11] = 101 - target[10]

        for piece in self.pieces[1:]:
            if piece[1] == head[1]:
                if piece[0] < head[0]:
                    target[12] = 1
                    diff = head[0] - piece[0]
                    if target[16] == 0 or diff < target[16]:
                        target[16] = diff
                elif piece[0] > head[0]:
                    target[13] = 1
                    diff = piece[0] - head[0]
                    if target[17] == 0 or diff < target[17]:
                        target[17] = diff

            if piece[0] == head[0]:
                if piece[1] < head[1]:
                    target[14] = 1
                    diff = head[1] - piece[1]
                    if target[18] == 0 or diff < target[18]:
                        target[18] = diff
                elif piece[1] > head[1]:
                    target[15] = 1
                    diff = piece[1] - head[1]
                    if target[19] == 0 or diff < target[19]:
                        target[19] = diff

        # Call brain's predict.
        return self.brain.activate(target)
