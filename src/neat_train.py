# Native Libraries
import pickle

# External Libraries
import neat
import numpy as np

# Local files
from neat_snek import Snek


def eval_sneks(genomes=None, config=None):
    # Generate 100 games each with 10000 different food configurations for the Sneks to play in.
    food = []
    for _ in range(100):
        game = []
        for _ in range(10000):
            game.append((np.random.randint(low=0, high=99), np.random.randint(low=0, high=99)))
        food.append(game)

    # For every genome, play.
    for _, genome in genomes:
        # Load the genome into a Neural Network.
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        scores = []
        for game in food:
            # At the start of each game, create a Snek with the Neural Network.
            snek = Snek(net)
            current_food_index = 0
            while current_food_index < 10000:
                # End current game when the Snek dies.
                if not snek.alive:
                    break

                # Snek uses Neural Network to predict the best direction to move at and does so.
                direction = np.argmax(snek.predict(game[current_food_index]))
                snek.move(direction, game[current_food_index])

                # Check if Snek is alive.
                snek.check_collision()

                # Check if Snek has just ate.
                if snek.pieces[0] == game[current_food_index]:
                    snek.eat()
                    current_food_index += 1

            scores.append(snek.points)

        # The fitness of the genome is the mean of the scores of the 100 games.
        genome.fitness = np.mean(scores)


def run(config_file):
    # Load config file.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population.
    p = neat.Population(config)

    # Report progress of the evolution.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 1000 generations.
    winner = p.run(eval_sneks, 1000)

    # Save the winning species.
    with open('winner.pkl', 'wb') as output:
        pickle.dump(winner, output, 1)


if __name__ == '__main__':
    run('neat.config')
