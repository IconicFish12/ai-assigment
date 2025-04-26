import random

def crossover(parent1, parent2, pc=0.9):
    if random.random() < pc:
        child1 = [(p1 + p2) / 2 for p1, p2 in zip(parent1["gen"], parent2["gen"])]
        child2 = [(p1 * 0.7 + p2 * 0.3) for p1, p2 in zip(parent1["gen"], parent2["gen"])]
        return [{"gen": child1, "fitness": None}, {"gen": child2, "fitness": None}]
    else:
        return [parent1.copy(), parent2.copy()]
