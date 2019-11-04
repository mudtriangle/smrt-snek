from snek import Snek
import numpy as np

NUM_SNEKS = 100
NUM_PARENTS = 1
NUM_GENS = 1000
MAX_MOVES = 1000000

sneks = []
food = []
for i in range(NUM_SNEKS):
    sneks.append(Snek())
    food.append((int(np.random.uniform(low=0, high=99)), int(np.random.uniform(low=0, high=99))))

for generation in range(NUM_GENS):
    for _ in range(MAX_MOVES):
        dead_count = 0
        for snek in sneks:
            if not snek.alive:
                dead_count += 1
        if dead_count == len(sneks):
            break

        for i in range(len(sneks)):
            if not sneks[i].alive:
                continue

            direction = np.argmax(sneks[i].predict(food[i]))
            sneks[i].move(direction)
            sneks[i].check_collision()

            if sneks[i].pieces[0] == food[i]:
                sneks[i].eat()
                food[i] = (int(np.random.uniform(low=0, high=99)), int(np.random.uniform(low=0, high=99)))

    points = []
    for snek in sneks:
        points.append(snek.points)
    highest_points = sorted(range(len(points)), key=lambda x: points[x])[-NUM_PARENTS:]

    print('Generation %i: ' % (generation + 1))
    print('    Average points: %.2f.' % (np.mean(points)))
    print('    Parent(s) for future generations:')
    parents = []
    for ind in highest_points:
        print('        Snek %i: %i points.' % (ind, points[ind]))
        parents.append(sneks[ind])

    sneks = []
    food = []
    for ind in range(len(parents)):
        parents[ind].reset()
        sneks.append(parents[ind])
        food.append((int(np.random.uniform(low=0, high=99)), int(np.random.uniform(low=0, high=99))))

    for i in range(NUM_SNEKS - NUM_PARENTS):
        sneks.append(Snek())
        sneks[i].update(parents)
        food.append((int(np.random.uniform(low=0, high=99)), int(np.random.uniform(low=0, high=99))))
