from src.ga_main import GeneticAlgorithm
from src.fitness import objective_function

if __name__ == "__main__":
    ga = GeneticAlgorithm()
    best = ga.run()

    print("\n✅ Solusi Terbaik:")
    print(f"  x1 = {best['gen'][0]:.6f}")
    print(f"  x2 = {best['gen'][1]:.6f}")
    print(f"  Fitness = {best['fitness']:.6f}")
    print(f"  f(x1, x2) = {objective_function(best['gen'][0], best['gen'][1]):.6f}")
