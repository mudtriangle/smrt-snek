from snek import Snek
import numpy as np

# Constants for training.
NUM_SNEKS = 100
NUM_PARENTS = 1
NUM_GENS = 1000
MAX_MOVES = 1000000

# Objects to be trained on.
sneks = []
food = []
for i in range(NUM_SNEKS):
    sneks.append(Snek())
    food.append((int(np.random.uniform(low=0, high=99)), int(np.random.uniform(low=0, high=99))))

# Summary after training.
bests = []
avgs = []

# Loop for each generation.
for generation in range(NUM_GENS):
    # Loop for the sneks to play during each generation. Limited by MAX_MOVES.
    for _ in range(MAX_MOVES):
        # End generation when all sneks are dead.
        dead_count = 0
        for snek in sneks:
            if not snek.alive:
                dead_count += 1
        if dead_count == len(sneks):
            break

        # In each step, make a move with each snek.
        for i in range(len(sneks)):
            # If the snek is dead, ignore.
            if not sneks[i].alive:
                continue

            # Use snek's brain to decide which direction to move in.
            direction = np.argmax(sneks[i].predict(food[i]))

            # Execute the move and check whether the snek dies.
            sneks[i].move(direction)
            sneks[i].check_collision()

            # Check if snek eats at after a move.
            if sneks[i].pieces[0] == food[i]:
                # If it does, generate new food position.
                sneks[i].eat()
                food[i] = (int(np.random.uniform(low=0, high=99)), int(np.random.uniform(low=0, high=99)))

    # List all points obtained by the sneks in the generation.
    points = []
    for snek in sneks:
        points.append(snek.points)

    # List the indices of the parents based on the top NUM_PARENTS points scored by the sneks.
    highest_points = sorted(range(len(points)), key=lambda x: points[x])[-NUM_PARENTS:]

    # Add info of the best snek to bests and add the generational average.
    bests.append(highest_points[-1])
    avgs.append(np.mean(points))

    # Summary of the generation.
    print('Generation %i: ' % (generation + 1))
    print('    Average points: %.2f.' % (np.mean(points)))
    print('    Parent(s) for future generations:')

    # List the sneks that will become parents of the next generation.
    parents = []
    for ind in highest_points:
        print('        Snek %i: %i points.' % (ind, points[ind]))
        parents.append(sneks[ind])

    # Save the parent sneks to play in next generation.
    sneks = []
    food = []
    for ind in range(len(parents)):
        parents[ind].reset()
        sneks.append(parents[ind])
        food.append((int(np.random.uniform(low=0, high=99)), int(np.random.uniform(low=0, high=99))))

    # Populate the rest of the generation with offsprings.
    for i in range(NUM_SNEKS - NUM_PARENTS):
        sneks.append(Snek())
        sneks[i].update(parents)
        food.append((int(np.random.uniform(low=0, high=99)), int(np.random.uniform(low=0, high=99))))

# Summary of the entire training.
print(bests)
print(avgs)
