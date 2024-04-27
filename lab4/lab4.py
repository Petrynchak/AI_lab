import random
import numpy as np
import json
import matplotlib.pyplot as plt

def plot_best_path(best_path, cities):
    plt.figure()
    X, Y = [], []
    for i in best_path:
        x_coord, y_coord = cities[i]
        X.append(x_coord)
        Y.append(y_coord)
    plt.plot(X, Y, '-o')
    plt.title('Найкращий шлях')
    plt.xlabel('X координата')
    plt.ylabel('Y координата')
    plt.show()

def generate_map(num_cities):
    cities = {}
    for i in range(num_cities):
        x_coord, y_coord = random.randint(0, 100), random.randint(0, 100)
        cities[i] = (x_coord, y_coord)
    return cities

# Збереження мапи у файл
def save_map(filename, cities):
    with open(filename, 'w') as file:
        json.dump(cities, file)

# Завантаження мапи з файлу
def load_map(filename):
    with open(filename, 'r') as file:
        cities_str = json.load(file)
    cities = {int(k): tuple(map(int, v)) for k, v in cities_str.items()}
    return cities

# Мурашиний алгоритм
def ant_colony(cities, num_ants, evaporation_rate, a, b, iterations, stagnation_limit=50):
    num_cities = len(cities)
    pheromones = np.ones((num_cities, num_cities))

    best_distance = float('inf')
    stagnation_count = 0
    best_iteration = 0

    for iteration in range(iterations):
        ants_paths = []

        for _ in range(num_ants):
            start_city = random.randint(0, num_cities - 1)
            current_city = start_city
            path = [current_city]

            while len(path) < num_cities:
                probabilities = []

                for city, coords in cities.items():
                    if city not in path:
                        distance = int(((coords[0] - cities[current_city][0]) ** 2 + (
                                    coords[1] - cities[current_city][1]) ** 2) ** 0.5)

                        visibility = 1 / distance
                        probability = (pheromones[current_city][city] * a) * (visibility ** b)
                        probabilities.append((city, probability))

                probabilities = np.array(probabilities)
                probabilities[:, 1] /= probabilities[:, 1].sum()

                next_city = np.random.choice(probabilities[:, 0].astype(int), p=probabilities[:, 1])
                path.append(next_city)
                current_city = next_city

            ants_paths.append(path)

        pheromones *= (1 - evaporation_rate)

        for path in ants_paths:
            path_length = sum(int(((cities[path[i - 1]][0] - cities[path[i]][0])**2 +
                                    (cities[path[i - 1]][1] - cities[path[i]][1])**2)**0.5)
                                    for i in range(1, len(path)))
            for i in range(1, len(path)):
                pheromones[path[i - 1]][path[i]] += 1 / path_length

        current_best_distance = min(sum(int(((cities[path[i - 1]][0] - cities[path[i]][0])**2 +
                                             (cities[path[i - 1]][1] - cities[path[i]][1])**2)**0.5)
                                             for i in range(1, len(x))) for x in ants_paths)

        if current_best_distance >= best_distance:
            stagnation_count += 1
        else:
            best_distance = current_best_distance
            stagnation_count = 0
            best_iteration = iteration

        if stagnation_count >= stagnation_limit:
            print(f"Алгоритм зупинено на ітерації {iteration}, стагнація протягом {stagnation_limit} ітерацій.")
            break

    best_path = min(ants_paths, key=lambda x: sum(int(((cities[x[i - 1]][0] - cities[x[i]][0])**2 +
                                                        (cities[x[i - 1]][1] - cities[x[i]][1])**2)**0.5)
                                                        for i in range(1, len(x))))

    return best_path, sum(int(((cities[best_path[i - 1]][0] - cities[best_path[i]][0])**2 +
                               (cities[best_path[i - 1]][1] - cities[best_path[i]][1])**2)**0.5)
                               for i in range(1, len(best_path)))

if __name__ == '__main__':
    num_cities = 25

    # Згенеруємо та збережемо нову мапу
    cities = generate_map(num_cities)
    save_map('map.json', cities)

    # Завантажимо мапу з файлу
    cities = load_map('map.json')

    num_ants = 10
    evaporation_rate = 0.5
    a = 1
    b = 5
    iterations = 1000

    total_best_distance = 0
    best_distances = []

    for simulation in range(10):
        print(f'\nСимуляція {simulation + 1}:')

        best_path, best_distance = ant_colony(cities, num_ants, evaporation_rate, a, b, iterations)
        print(f'Найкращий маршрут: {best_path}')
        print(f'Найкраща відстань: {best_distance} одиниць')

        plot_best_path(best_path, cities)

        total_best_distance += best_distance
        best_distances.append(best_distance)

    average_best_distance = total_best_distance / 10
    print(f'\nСередня найкраща відстань за 10 симуляцій: {average_best_distance} одиниць')

    min_distance = min(best_distances)
    max_distance = max(best_distances)

    print(f'Мінімальна відстань: {min_distance} одиниць')
    print(f'Максимальна відстань: {max_distance} одиниць')
