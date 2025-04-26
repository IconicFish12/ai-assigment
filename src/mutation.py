import random

def mutate(individu, pm=0.1):
    for i in range(len(individu["gen"])):
        if random.random() < pm:
            individu["gen"][i] += random.uniform(-1, 1)
            individu["gen"][i] = max(-10, min(10, individu["gen"][i]))
