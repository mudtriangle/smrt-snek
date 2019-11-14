import neat
import pickle
import numpy as np
from neat_snek import Snek


def eval_sneks(genomes=None, config=None):
    food = []
    for _ in range(10000):
        food.append((np.random.randint(low=0, high=99), np.random.randint(low=0, high=99)))

    for _, genome in genomes:
        current_food_index = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        snek = Snek(net)

        while current_food_index < 10000:
            if not snek.alive:
                break

            # print(snek.predict(food[current_food_index]))
            direction = np.argmax(snek.predict(food[current_food_index]))
            snek.move(direction)
            snek.check_collision()
            if snek.pieces[0] == food[current_food_index]:
                snek.eat()
                current_food_index += 1

        genome.fitness = snek.points


def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 300 generations.
    winner = p.run(eval_sneks, 300)

    with open('winner.pkl', 'wb') as output:
        pickle.dump(winner, output, 1)


if __name__ == '__main__':
    run('neat.config')
