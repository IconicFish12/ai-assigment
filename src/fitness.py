import math

def objective_function(x1, x2):
    try:
        return -(
            math.sin(x1) * math.cos(x2) * math.tan(x1 + x2) +
            (3 / 4) * math.exp(1 - math.sqrt(x1 ** 2))
        )
    except:
        return float('inf')

def evaluate_fitness(individu):
    x1, x2 = individu["gen"]
    val = objective_function(x1, x2)
    individu["fitness"] = 1 / (1 + abs(val))

def evaluate_population(pop):
    for individu in pop:
        evaluate_fitness(individu)
