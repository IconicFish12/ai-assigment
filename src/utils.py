import random

def generate_initial_population(pop_size):
    population = []
    for _ in range(pop_size):
        x1 = random.uniform(-10, 10)
        x2 = random.uniform(-10, 10)
        population.append({"gen": [x1, x2], "fitness": None})
    return population

def next_generation(old_pop, offspring, elite_size=2):
    total = old_pop + offspring
    total.sort(key=lambda ind: ind["fitness"], reverse=True)
    return total[:len(old_pop)]
