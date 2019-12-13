# Native Libraries
import pickle

# External Libraries
import arcade
import neat
import numpy as np

# Local files
from neat_snek import Snek

# Constants for the window.
SCREEN_WIDTH = 1430
SCREEN_HEIGHT = 710
SCREEN_TITLE = "Smart Snek"

# Constants for the colors.
COLORS = [(240, 234, 214), (12, 10, 4), (255, 0, 0)]

# Load the model into a Snek.
with open('winner.pkl', 'rb') as f:
    genome = pickle.load(f)
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     'neat.config')
model = neat.nn.FeedForwardNetwork.create(genome, config)
snek = Snek(model)


# Function for drawing the board.
def get_shape(board, x_offset, y_offset, square_size, square_spacing):
    point_list = []
    color_list = []

    for x in range(100):
        for y in range(100):
            # Used points instead of squares to draw on screen faster.
            top_left = (x * square_spacing + x_offset, SCREEN_HEIGHT - y * square_spacing - y_offset)
            top_right = (top_left[0] + square_size, top_left[1])
            bottom_right = (top_right[0], top_right[1] - square_size)
            bottom_left = (top_left[0], bottom_right[1])

            point_list.append(top_left)
            point_list.append(top_right)
            point_list.append(bottom_right)
            point_list.append(bottom_left)

            for _ in range(4):
                # Add the color of the block depending on what is in it on the board.
                color_list.append(COLORS[board[y][x]])

    # Return Arcade rectangles.
    return arcade.create_rectangles_filled_with_colors(point_list, color_list)


# Function for updating the game at each step.
def update_game(board, snek, alive, direction, food):
    # Do not update if Snek is dead.
    if not alive:
        return board, snek, alive, food

    # New elements of the game.
    new_board = np.zeros(board.shape, dtype=int)
    new_snek = []
    new_alive = True
    new_food = food

    # Move the Snek in a given direction.
    if direction == 0:
        new_snek = [(snek[0][0], snek[0][1] + 1)] + snek[: -1]
        if new_snek[0][1] > 99:
            new_snek[0] = (new_snek[0][0], 99)
            new_alive = False

    elif direction == 1:
        new_snek = [(snek[0][0], snek[0][1] - 1)] + snek[: -1]
        if new_snek[0][1] < 0:
            new_snek[0] = (new_snek[0][0], 0)
            new_alive = False

    elif direction == 2:
        new_snek = [(snek[0][0] + 1, snek[0][1])] + snek[: -1]
        if new_snek[0][0] > 99:
            new_snek[0] = (99, new_snek[0][1])
            new_alive = False

    elif direction == 3:
        new_snek = [(snek[0][0] - 1, snek[0][1])] + snek[: -1]
        if new_snek[0][0] < 0:
            new_snek[0] = (0, new_snek[0][1])
            new_alive = False

    # If the Snek stepped on its own tail, game is over.
    if new_snek[0] in new_snek[1:]:
        new_alive = False

    # If the Snek ate food, increase its length by 1.
    if food == new_snek[0]:
        new_snek.append(snek[-1])
        while True:
            new_food = (int(np.random.uniform(0, 99)), int(np.random.uniform(0, 99)))
            if new_food[0] != food[0] and new_food[1] != food[1]:
                break

    # Populate the board.
    for x in range(new_board.shape[0]):
        for y in range(new_board.shape[1]):
            if (x, y) in new_snek:
                new_board[x][y] = 1

            elif (x, y) == new_food:
                new_board[x][y] = 2

    return new_board, new_snek, new_alive, new_food


# Class that handles game interactions.
class Game(arcade.Window):
    def __init__(self, width, height, title):
        # Initial conditions of the game.
        super().__init__(width, height, title, update_rate=1/20)

        arcade.set_background_color((255, 255, 255))

        self.shape_list = None

        self.board_ai = np.zeros((100, 100), dtype=int)
        self.board_player = np.zeros((100, 100), dtype=int)

        self.direction_ai = 0
        self.direction_player = 0

        self.pieces_ai = [(0, 2), (0, 1), (0, 0)]
        self.pieces_player = [(0, 2), (0, 1), (0, 0)]

        # Food is initiated randomly.
        self.food_ai = (int(np.random.uniform(0, 99)), int(np.random.uniform(0, 99)))
        self.food_player = (int(np.random.uniform(0, 99)), int(np.random.uniform(0, 99)))

        self.alive_ai = True
        self.alive_player = True

        self.score_ai = 0
        self.score_player = 0

    def setup(self):
        # Called at the start of the game and on every reset.
        self.alive_ai = True
        self.alive_player = True

        self.direction_ai = 0
        self.direction_player = 0

        self.pieces_ai = [(0, 2), (0, 1), (0, 0)]
        self.pieces_player = [(0, 2), (0, 1), (0, 0)]

        self.pieces_ai = [(0, 2), (0, 1), (0, 0)]
        self.pieces_player = [(0, 2), (0, 1), (0, 0)]

        self.food_ai = (int(np.random.uniform(0, 99)), int(np.random.uniform(0, 99)))
        self.food_player = (int(np.random.uniform(0, 99)), int(np.random.uniform(0, 99)))

        # Shapes for initial drawing.
        self.shape_list = arcade.ShapeElementList()

        self.shape_list.append(get_shape(self.board_ai, 5, 5, 5, 7))
        self.shape_list.append(get_shape(self.board_player, 725, 5, 5, 7))

        # Initial scores.
        self.score_ai = len(self.pieces_ai) - 3
        self.score_player = len(self.pieces_player) - 3

    def on_draw(self):
        # Draw on screen.
        arcade.start_render()
        arcade.draw_rectangle_filled(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, (255, 255, 255))
        self.shape_list.draw()

        # Display points.
        arcade.draw_text('Points: %i' % self.score_ai, 5, 5, (0, 0, 0), 12)
        arcade.draw_text('Points: %i' % self.score_player, 1425, 5, (0, 0, 0), 12, anchor_x='right')

    def on_key_press(self, key, modifiers):
        # For user interaction, on key pressed, change direction.
        if key == arcade.key.UP and self.direction_player != 2:
            self.direction_player = 3

        elif key == arcade.key.DOWN and self.direction_player != 3:
            self.direction_player = 2

        elif key == arcade.key.LEFT and self.direction_player != 0:
            self.direction_player = 1

        elif key == arcade.key.RIGHT and self.direction_player != 1:
            self.direction_player = 0

        # Press R to reset.
        elif key == arcade.key.R:
            self.setup()

    def update(self, delta_time):
        # Call the Snek model to determine the direction of the AI Snek.
        if self.alive_ai:
            snek.pieces = self.pieces_ai
            pred = snek.predict(self.food_ai, self.direction_ai)
            direction = np.argmax(pred)

            if direction == 3 and self.direction_ai != 2:
                self.direction_ai = 3

            elif direction == 2 and self.direction_ai != 3:
                self.direction_ai = 2

            elif direction == 1 and self.direction_ai != 0:
                self.direction_ai = 1

            elif direction == 0 and self.direction_ai != 1:
                self.direction_ai = 0

        # Update both the AI board and the player board.
        self.board_ai, self.pieces_ai, self.alive_ai, self.food_ai = update_game(self.board_ai, self.pieces_ai,
                                                                                 self.alive_ai, self.direction_ai,
                                                                                 self.food_ai)

        self.board_player, self.pieces_player, self.alive_player, self.food_player = update_game(self.board_player,
                                                                                                 self.pieces_player,
                                                                                                 self.alive_player,
                                                                                                 self.direction_player,
                                                                                                 self.food_player)

        # Reload shapes for drawing.
        self.shape_list = arcade.ShapeElementList()

        self.shape_list.append(get_shape(self.board_ai, 5, 5, 5, 7))
        self.shape_list.append(get_shape(self.board_player, 725, 5, 5, 7))

        # Update scores if relevant.
        self.score_ai = len(self.pieces_ai) - 3
        self.score_player = len(self.pieces_player) - 3


def main():
    window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
