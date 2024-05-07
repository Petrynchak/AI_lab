import random
import json

# Константи для налаштування алгоритму
NUM_LESSONS = 5  # Кількість різних уроків (зменшено)
TOTAL_LESSONS_PER_WEEK = 25  # Загальна кількість уроків на тиждень
NUM_TEACHERS = 5  # Кількість різних вчителів
NUM_CLASSES = 2  # Кількість класів
MAX_LESSONS_PER_DAY = 5  # Максимальна кількість уроків на день
DAYS_PER_WEEK = 5  # Кількість днів навчання в тиждень

# Назви звичайних уроків
LESSON_NAMES = [
    'Математика',
    'Українська мова',
    'Англійська мова',
    'Фізика',
    'Хімія'
]

# Назви спеціальних уроків
SPECIAL_LESSONS = [
    'Фізвиховання',
    'Хореографія',
    'Музика'
]

# Вчителі та їх спеціалізації
TEACHERS = {
    'Класний керівник 1': ['Математика', 'Фізика', 'Англійська мова'],
    'Класний керівник 2': ['Українська мова', 'Історія', 'Хімія'],
    'Вчитель 3': ['Географія'],
    'Вчитель 4': ['Біологія'],
    'Вчитель 5': ['Фізвиховання', 'Хореографія', 'Музика']  # Додано нового вчителя
}

# Функції для запису та читання даних
def save_data_to_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def load_data_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

# Структура хромосоми
class Chromosome:
    def init(self):
        self.genes = []  # Гени хромосоми
        self.fitness = 0  # Цільова функція

    def generate_initial_genes(self):
        # Генерація початкових генів для кожного класу
        for class_num in range(NUM_CLASSES):
            class_genes = []
            for _ in range(DAYS_PER_WEEK):
                # Генерація уроків для одного дня
                day_lessons = random.sample(LESSON_NAMES + SPECIAL_LESSONS, MAX_LESSONS_PER_DAY)
                # Додаємо уроки від класного керівника
                head_teacher_lessons = [lesson for lesson in day_lessons if lesson in TEACHERS[f'Класний керівник {class_num + 1}']]
                # Якщо уроків від класного керівника менше половини, додаємо їх
                while len(head_teacher_lessons) < MAX_LESSONS_PER_DAY // 2:
                    lesson_to_add = random.choice(TEACHERS[f'Класний керівник {class_num + 1}'])
                    if lesson_to_add not in head_teacher_lessons:
                        head_teacher_lessons.append(lesson_to_add)
                # Додаємо решту уроків
                class_genes.extend(head_teacher_lessons)
                class_genes.extend([lesson for lesson in day_lessons if lesson not in head_teacher_lessons])
            self.genes.append(class_genes)
        self.calculate_fitness()

    def calculate_fitness(self):
        # Обчислення значення цільової функції
        fitness = 0
        for class_genes in self.genes:
            daily_lessons = [class_genes[i:i + MAX_LESSONS_PER_DAY] for i in range(0, len(class_genes), MAX_LESSONS_PER_DAY)]
            for day in daily_lessons:
                unique_lessons = set(day)
                fitness += len(unique_lessons)  # Більше унікальних уроків - краще
        self.fitness = fitness

    def mutate(self):
        # Мутація випадкового класу
        class_index = random.randint(0, NUM_CLASSES - 1)
        index1, index2 = random.sample(range(len(self.genes[class_index])), 2)
        self.genes[class_index][index1], self.genes[class_index][index2] = self.genes[class_index][index2], self.genes[class_index][index1]
        self.calculate_fitness()

    def crossover(self, other):
        # Схрещування з іншою хромосомою
        child = Chromosome()
        for i in range(NUM_CLASSES):
            if random.random() > 0.5:
                child.genes.append(self.genes[i])
            else:
                child.genes.append(other.genes[i])
        child.calculate_fitness()
        return child

# Функції для запису та читання даних
def save_data_to_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

        def load_data_from_file(filename):
            with open(filename, 'r', encoding='utf-8') as file:
                return json.load(file)

        # Реалізація генетичного алгоритму
        class GeneticAlgorithm:
            def init(self):
                self.population = []

            def initialize_population(self):
                for _ in range(10):
                    chromosome = Chromosome()
                    chromosome.generate_initial_genes()
                    self.population.append(chromosome)

            def run(self):
                for generation in range(100):
                    self.population.sort(key=lambda x: x.fitness, reverse=True)
                    new_generation = []
                    while len(new_generation) < 10:
                        parent1, parent2 = random.sample(self.population, 2)
                        child = parent1.crossover(parent2)
                        child.mutate()
                        new_generation.append(child)
                    self.population = new_generation
                best_chromosome = self.population[0]  # Припустимо, що це найкраща хромосома
                schedule = {'schedule': best_chromosome.genes}
                save_data_to_file(schedule, 'schedule.json')

            def print_best_schedule(self):
                best_chromosome = max(self.population, key=lambda x: x.fitness)
                for class_index, class_genes in enumerate(best_chromosome.genes):
                    print(f'Розклад для класу {class_index + 1}:')
                    for day in range(DAYS_PER_WEEK):
                        print(
                            f'  День {day + 1}: {class_genes[day * MAX_LESSONS_PER_DAY:(day + 1) * MAX_LESSONS_PER_DAY]}')

        # Основна програма
        def main():
            ga = GeneticAlgorithm()
            ga.initialize_population()
            ga.run()
            ga.print_best_schedule()
            loaded_schedule = load_data_from_file('schedule.json')
            print(loaded_schedule)

        if __name__ == '__main__':
            main()
