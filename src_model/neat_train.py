import neat
import pickle
import numpy as np
from neat_snek import Snek


def eval_sneks(genomes=None, config=None):
    food = []
    game = []
    for _ in range(100):
        for _ in range(10000):
            game.append((np.random.randint(low=0, high=99), np.random.randint(low=0, high=99)))
        food.append(game)

    for _, genome in genomes:
        current_food_index = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        snek = Snek(net)

        scores = []
        for game in food:
            while current_food_index < 10000:
                if not snek.alive:
                    break

                direction = np.argmax(snek.predict(game[current_food_index]))
                snek.move(direction, game[current_food_index])
                snek.check_collision()
                if snek.pieces[0] == game[current_food_index]:
                    snek.eat()
                    current_food_index += 1

            scores.append(snek.points)

        genome.fitness = np.mean(scores)


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

    # Run for up to 1000 generations.
    winner = p.run(eval_sneks, 1000)

    with open('winner.pkl', 'wb') as output:
        pickle.dump(winner, output, 1)


if __name__ == '__main__':
    run('neat.config')
