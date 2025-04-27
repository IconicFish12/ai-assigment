import math
import random

# ========================================
# Parameter GA
# ========================================
N_BITS = 16          # jumlah bit per variabel
LOWER_BOUND = -10     # batas bawah domain
UPPER_BOUND = 10      # batas atas domain
CHROMOSOME_LENGTH = N_BITS * 2

# ========================================
# 1. Inisialisasi Populasi
# ========================================
def generate_initial_population(pop_size):
    """
    Membuat populasi awal: list of individu dengan kromosom biner acak.
    Setiap individu: {'gen': str, 'fitness': float, 'f_val': float}
    """
    population = []
    for _ in range(pop_size):
        gene = ''.join(random.choice('01') for _ in range(CHROMOSOME_LENGTH))
        population.append({'gen': gene, 'fitness': None, 'f_val': None})
    return population

# ========================================
# 2. Decode Kromosom
# ========================================
def decode_chromosome(ind):
    """
    Memecah kromosom jadi dua variabel, konversi ke desimal,
    lalu mapping ke domain [LOWER_BOUND, UPPER_BOUND].
    """
    g = ind['gen']
    bin_x1, bin_x2 = g[:N_BITS], g[N_BITS:]
    int_x1, int_x2 = int(bin_x1, 2), int(bin_x2, 2)
    max_int = 2**N_BITS - 1
    x1 = LOWER_BOUND + (int_x1 / max_int) * (UPPER_BOUND - LOWER_BOUND)
    x2 = LOWER_BOUND + (int_x2 / max_int) * (UPPER_BOUND - LOWER_BOUND)
    return x1, x2

# ========================================
# 3. Fungsi Objektif & Fitness
# ========================================
def objective_function(x1, x2):
    """
    g(x1,x2) = sin(x1)*cos(x2)*tan(x1+x2) + 3/4 * exp(1 - |x1|)
    """
    try:
        return math.sin(x1) * math.cos(x2) * math.tan(x1 + x2) + \
               (3/4) * math.exp(1 - abs(x1))
    except:
        return float('inf')

def calculate_fitness(ind):
    x1, x2 = decode_chromosome(ind)
    f_val = objective_function(x1, x2)
    ind['f_val'] = f_val
    ind['fitness'] = 1 / (1 + abs(f_val))  # untuk minimisasi
    return ind['fitness']

# ========================================
# 4. Seleksi Orangtua (Tournament)
# ========================================
def tournament_selection(population, k=3):
    """
    Pilih kandidat k acak, kembalikan yang fitness-nya tertinggi.
    """
    contestants = random.sample(population, k)
    return max(contestants, key=lambda ind: ind['fitness'])

# ========================================
# 5. Crossover (Single-Point)
# ========================================
def crossover(p1, p2, crossover_rate=0.9):
    if random.random() < crossover_rate:
        point = random.randint(1, CHROMOSOME_LENGTH - 1)
        c1 = p1['gen'][:point] + p2['gen'][point:]
        c2 = p2['gen'][:point] + p1['gen'][point:]
    else:
        c1, c2 = p1['gen'], p2['gen']
    return [
        {'gen': c1, 'fitness': None, 'f_val': None},
        {'gen': c2, 'fitness': None, 'f_val': None}
    ]

# ========================================
# 6. Mutasi (Flip Bit)
# ========================================
def mutate(ind, mutation_rate=0.01):
    bits = list(ind['gen'])
    for i in range(len(bits)):
        if random.random() < mutation_rate:
            bits[i] = '1' if bits[i] == '0' else '0'
    ind['gen'] = ''.join(bits)
    ind['fitness'] = None
    ind['f_val'] = None

# ========================================
# 7. Seleksi Survivor (Elitism)
# ========================================
def next_generation(population, offspring, pop_size):
    combined = population + offspring
    combined = [ind for ind in combined if ind['fitness'] is not None]
    combined.sort(key=lambda ind: ind['fitness'], reverse=True)
    return combined[:pop_size]

# ========================================
# 8. Main GA
# ========================================
def genetic_algorithm(pop_size=100, generations=50, crossover_rate=0.9, mutation_rate=0.01, stagnation_limit=10):
    # Inisialisasi & Evaluasi Awal
    population = generate_initial_population(pop_size)
    for ind in population:
        calculate_fitness(ind)

    best_fitness_history = []
    stagnation_counter = 0

    # Evolusi
    for gen in range(1, generations + 1):
        offspring = []
        while len(offspring) < pop_size:
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)
            for child in crossover(parent1, parent2, crossover_rate):
                mutate(child, mutation_rate)
                calculate_fitness(child)
                offspring.append(child)
        population = next_generation(population, offspring[:pop_size], pop_size)
        best = min(population, key=lambda ind: ind['f_val'])
        x1, x2 = decode_chromosome(best)
        print(f"Gen {gen}: Best f(x) = {best['f_val']:.6f}, x1={x1:.4f}, x2={x2:.4f}")

        # Cek Stagnasi
        best_fitness = best['fitness']
        if best_fitness in best_fitness_history:
            stagnation_counter += 1
            if stagnation_counter >= stagnation_limit:
                print(f"\nEvolusi dihentikan karena stagnasi pada generasi {gen}.")
                break  # Keluar dari loop generasi
        else:
            stagnation_counter = 0
        best_fitness_history.append(best_fitness)
        best_fitness_history = best_fitness_history[-stagnation_limit:]  # Keep only the last few fitness values

    # Output Akhir: Generasi Terakhir
    best = min(population, key=lambda ind: ind['f_val'])
    x1, x2 = decode_chromosome(best)
    print("\n✅ Solusi Minimum Ditemukan pada Generasi Terakhir:")
    print(f" Chromosome = {best['gen']}")
    print(f" x1 = {x1:.6f}")
    print(f" x2 = {x2:.6f}")
    print(f" Minimum f(x1,x2) = {best['f_val']:.6f}")
    return best

if __name__ == "__main__":
    genetic_algorithm(stagnation_limit=20) 