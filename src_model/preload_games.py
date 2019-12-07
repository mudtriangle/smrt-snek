import pickle
from neat_snek import Snek
import neat
import numpy as np

with open('winner.pkl', 'rb') as f:
    genome = pickle.load(f)

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     'neat.config')
model = neat.nn.FeedForwardNetwork.create(genome, config)

i = 0
while i < 100:
    snek = Snek(model)
    print('Writing ../preloaded_games/game_' + str(i) + '.txt')
    with open('../preloaded_games/game_' + str(i) + '.txt', 'w') as f:
        food = []
        for _ in range(10000):
            food.append((np.random.randint(low=0, high=99), np.random.randint(low=0, high=99)))
        current_food_index = 0

        while snek.alive:
            direction = np.argmax(snek.predict(food[current_food_index]))

            f.write('%i %i %i\n' % (direction, food[current_food_index][0], food[current_food_index][1]))

            snek.move(direction)
            snek.check_collision()
            if snek.pieces[0] == food[current_food_index]:
                snek.eat()
                current_food_index += 1

    if snek.points > 50:
        print('    Valid. Writing next game.')
        i += 1
    else:
        print('    Score is not high enough. Rewriting.')
