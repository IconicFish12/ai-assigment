from src.fitness import evaluate_population, evaluate_fitness, objective_function
from src.selection import tournament_selection
from src.crossover import crossover
from src.mutation import mutate
from src.utils import generate_initial_population, next_generation

class GeneticAlgorithm:
    def __init__(self, pop_size=30, generations=50, pc=0.9, pm=0.1):
        self.pop_size = pop_size
        self.generations = generations
        self.pc = pc
        self.pm = pm
        self.population = []

    def run(self):
        self.population = generate_initial_population(self.pop_size)
        evaluate_population(self.population)

        for gen in range(self.generations):
            new_population = []
            while len(new_population) < self.pop_size:
                parent1 = tournament_selection(self.population)
                parent2 = tournament_selection(self.population)
                children = crossover(parent1, parent2, self.pc)
                for child in children:
                    mutate(child, self.pm)
                    evaluate_fitness(child)
                    new_population.append(child)
            self.population = next_generation(self.population, new_population)

            best = max(self.population, key=lambda ind: ind["fitness"])
            print(f"[Gen {gen+1}] Best fitness: {best['fitness']:.6f} | x1 = {best['gen'][0]:.4f}, x2 = {best['gen'][1]:.4f}")

        return max(self.population, key=lambda ind: ind["fitness"])
