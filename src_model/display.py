import arcade
import numpy as np
import pickle
import neat
from neat_snek import Snek

SCREEN_WIDTH = 1430
SCREEN_HEIGHT = 710
SCREEN_TITLE = "Smart Snek"

COLORS = [(240, 234, 214), (12, 10, 4), (255, 0, 0)]

with open('winner.pkl', 'rb') as f:
    genome = pickle.load(f)

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     'neat.config')
model = neat.nn.FeedForwardNetwork.create(genome, config)
snek = Snek(model)


def get_shape(board, x_offset, y_offset, square_size, square_spacing):
    point_list = []
    color_list = []

    for x in range(100):
        for y in range(100):
            top_left = (x * square_spacing + x_offset, SCREEN_HEIGHT - y * square_spacing - y_offset)
            top_right = (top_left[0] + square_size, top_left[1])
            bottom_right = (top_right[0], top_right[1] - square_size)
            bottom_left = (top_left[0], bottom_right[1])

            point_list.append(top_left)
            point_list.append(top_right)
            point_list.append(bottom_right)
            point_list.append(bottom_left)

            for _ in range(4):
                color_list.append(COLORS[board[y][x]])

    return arcade.create_rectangles_filled_with_colors(point_list, color_list)


def update_game(board, snek, alive, direction, food):
    if not alive:
        return board, snek, alive, food

    new_board = np.zeros(board.shape, dtype=int)
    new_snek = []
    new_alive = True
    new_food = food
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
        if new_snek[0][1] > 99:
            new_snek[0] = (99, new_snek[0][1])
            new_alive = False

    elif direction == 3:
        new_snek = [(snek[0][0] - 1, snek[0][1])] + snek[: -1]
        if new_snek[0][1] < 0:
            new_snek[0][1] = (0, new_snek[0][1])
            new_alive = False

    if new_snek[0] in new_snek[1:]:
        new_alive = False

    if food == new_snek[0]:
        new_snek.append(snek[-1])
        new_food = (int(np.random.uniform(0, 99)), int(np.random.uniform(0, 99)))

    for x in range(board.shape[0]):
        for y in range(board.shape[1]):
            if (x, y) in new_snek:
                board[x][y] = 2

            elif (x, y) == new_food:
                board[x][y] = 1

    return new_board, new_snek, new_alive, new_food


class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, update_rate=1/10)

        arcade.set_background_color((255, 255, 255))

        self.draw_time = 0
        self.shape_list = None

        self.board_ai = np.zeros((100, 100), dtype=int)
        self.board_player = np.zeros((100, 100), dtype=int)

        self.direction_ai = 0
        self.direction_player = 0

        self.pieces_ai = [(0, 2), (0, 1), (0, 0)]
        self.pieces_player = [(0, 2), (0, 1), (0, 0)]

        self.food_ai = (int(np.random.uniform(0, 99)), int(np.random.uniform(0, 99)))
        self.food_player = (int(np.random.uniform(0, 99)), int(np.random.uniform(0, 99)))

        self.alive_ai = True
        self.alive_player = True

    def setup(self):
        self.board_ai, self.pieces_ai, self.alive_ai, self.food_ai = update_game(self.board_ai, self.pieces_ai,
                                                                                 self.alive_ai, self.direction_ai,
                                                                                 self.food_ai)

        self.board_player, self.pieces_player, self.alive_player, self.food_player = update_game(self.board_player,
                                                                                                 self.pieces_player,
                                                                                                 self.alive_player,
                                                                                                 self.direction_player,
                                                                                                 self.food_player)

        self.shape_list = arcade.ShapeElementList()

        self.shape_list.append(get_shape(self.board_ai, 5, 5, 5, 7))
        self.shape_list.append(get_shape(self.board_player, 725, 5, 5, 7))

    def on_draw(self):
        arcade.start_render()
        self.shape_list.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP and self.direction_player != 2:
            self.direction_player = 3

        elif key == arcade.key.DOWN and self.direction_player != 3:
            self.direction_player = 2

        elif key == arcade.key.LEFT and self.direction_player != 0:
            self.direction_player = 1

        elif key == arcade.key.RIGHT and self.direction_player != 1:
            self.direction_player = 0

    def update(self, delta_time):
        direction = np.argmax(snek.predict(self.food_ai))
        snek.move(direction)
        self.direction_ai = direction
        print(direction)

        self.board_ai, self.pieces_ai, self.alive_ai, self.food_ai = update_game(self.board_ai, self.pieces_ai,
                                                                                 self.alive_ai, self.direction_ai,
                                                                                 self.food_ai)

        self.board_player, self.pieces_player, self.alive_player, self.food_player = update_game(self.board_player,
                                                                                                 self.pieces_player,
                                                                                                 self.alive_player,
                                                                                                 self.direction_player,
                                                                                                 self.food_player)

        self.shape_list = arcade.ShapeElementList()

        self.shape_list.append(get_shape(self.board_ai, 5, 5, 5, 7))
        self.shape_list.append(get_shape(self.board_player, 725, 5, 5, 7))


def main():
    window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    window.on_draw()
    arcade.run()


if __name__ == "__main__":
    main()
