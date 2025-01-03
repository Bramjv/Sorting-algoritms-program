import random
import time
import csv
import matplotlib.pyplot as plt
import heapq


# Funkcja do generowania danych
def generate_data_integer(size, order="random"):
    data = [random.randint(0, 1000) for _ in range(size)]
    #   data_type = "integer"
    if order == "sorted":
        data.sort()
    elif order == "reverse":
        data.sort(reverse=True)
    elif order == "partially sorted":
        partially_sorted_size = size // 2
        data[:partially_sorted_size] = sorted(data[:partially_sorted_size])

    return data


def generate_data_float(size, order="random"):
    data = [random.uniform(0, 1000) for _ in range(size)]
    #    data_type = "float"
    if order == "sorted":
        data.sort()
    elif order == "reverse":
        data.sort(reverse=True)
    elif order == "partially sorted":
        partially_sorted_size = size // 2
        data[:partially_sorted_size] = sorted(data[:partially_sorted_size])

    return data


# Implementacja Quick Sort
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = random.choice(arr)  # Losowy wybór pivota
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return quick_sort(left) + middle + quick_sort(right)


# Implementacja Merge Sort
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)


def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# Implementacja Tim Sort
def tim_sort(arr):
    arr.sort()  # Python używa Tim Sort wewnętrznie w metodzie .sort()
    return arr


# Implementacja Bucket Sort
def bucket_sort(arr):
    if len(arr) == 0:
        return arr

    min_val = min(arr)
    max_val = max(arr)
    bucket_count = len(arr)

    # Tworzenie koszyków
    buckets = [[] for _ in range(bucket_count)]

    # Umieszczanie elementów w koszykach
    for num in arr:
        index = int((num - min_val) / (max_val - min_val + 1) * (bucket_count - 1))
        buckets[index].append(num)

    # Sortowanie w każdym koszyku
    for i in range(bucket_count):
        buckets[i] = sorted(buckets[i])

    # Łączenie posortowanych elementów
    sorted_arr = []
    for bucket in buckets:
        sorted_arr.extend(bucket)

    return sorted_arr


# Implementacja Heap Sort
def heap_sort(arr):
    heapq.heapify(arr)  # Tworzy kopiec
    return [heapq.heappop(arr) for _ in range(len(arr))]


# Funkcja do mierzenia czasu sortowania
def measure_sort_time(sort_function, data):
    start_time = time.time()
    sort_function(data)
    end_time = time.time()
    return end_time - start_time


# Główna funkcja testująca i zapisująca wyniki
def run_tests_and_save_to_csv(output_file):
    counter = 0
    min_value = 100000
    max_value = 1000000
    data_sizes = [random.randint(min_value, max_value) for _ in range(3)]
    data_characteristics = ["random", "sorted", "reverse", "partially sorted"]
    sort_algorithms = {
        "Quick Sort": quick_sort,
        "Merge Sort": merge_sort,
        "Tim Sort": tim_sort,
        "Bucket Sort": bucket_sort,
        "Heap Sort": heap_sort
    }

    data_characteristics_length = len(data_characteristics)
    data_sizes_length = len(data_sizes)
    sort_algorithms_length = len(sort_algorithms)
    estimated_attempts = data_characteristics_length * data_sizes_length * sort_algorithms_length
    print(f"Program będzie potrzebował {estimated_attempts} prób aby posortować wszystkie tablice, wszystkimi "
          f"algorytmami w każdym podanym ułożeniu.")

    results_array = []

    with open(output_file, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(
            ["Proba", "Algorithm", "Data Size", "Data Characteristic", "Time (s)", "Data type(integer/float)"])

        for size in data_sizes:
            for characteristic in data_characteristics:
                for algo_name, algo_func in sort_algorithms.items():
                    data = generate_data_integer(size, characteristic)
                    time_taken = measure_sort_time(algo_func, data)
                    data_type = "integer"
                    counter += 1
                    writer.writerow([counter, algo_name, size, characteristic, time_taken, data_type])
                    results_array.append((counter, algo_name, size, characteristic, time_taken, data_type))
                    print(
                        f"(Próba: {counter}), Algorytm: {algo_name}, Rozmiar: {size}, Charakterystyka: {characteristic}"
                        f" ,Czas: {time_taken:.6f} sekund, Typ danych: integer")
                """ 
                for algo_name, algo_func in sort_algorithms.items():
                    data = generate_data_float(size, characteristic)
                    time_taken = measure_sort_time(algo_func, data)
                    data_type = "float"
                    counter += 1
                    writer.writerow([counter, algo_name, size, characteristic, time_taken, data_type])
                    results_array.append((counter, algo_name, size, characteristic, time_taken, data_type))
                    print(
                        f"(Próba: {counter}), Algorytm: {algo_name}, Rozmiar: {size}, Charakterystyka: {characteristic}"
                        f" ,Czas: {time_taken:.6f} sekund, Typ danych: float")
                """

    return results_array


# Funkcja do wizualizacji wyników
def visualize_results(results_array):
    algorithms = list(set(result[1] for result in results_array))
    data_sizes = sorted(list(set(result[2] for result in results_array)))
    characteristics = list(set(result[3] for result in results_array))

    for characteristic in characteristics:
        plt.figure(figsize=(10, 6))

        # Iterujemy przez wszystkie algorytmy
        for algo in algorithms:
            times = []
            # Zbieramy czas dla danego algorytmu i charakterystyki
            for size in data_sizes:
                # Wybieramy czas, który odpowiada rozmiarowi danych
                time_for_size = next(
                    (result[4] for result in results_array if
                     result[1] == algo and result[2] == size and result[3] == characteristic),
                    None
                )
                # Dodajemy czas do listy 'times'
                if time_for_size is not None:
                    times.append(time_for_size)

            # Sprawdzamy, czy mamy dane do narysowania wykresu
            if len(times) == len(data_sizes):
                plt.plot(data_sizes, times, marker='o', label=algo)
            else:
                print(f"Brak danych do wykresu dla algorytmu: {algo} i charakterystyki: {characteristic}")

        plt.title(f"Czas sortowania dla danych: {characteristic}")
        plt.xlabel("Rozmiar danych")
        plt.ylabel("Czas (s)")
        plt.legend()
        plt.grid()
        plt.show()


# Uruchomienie testów, zapisanie wyników i wizualizacja
results = run_tests_and_save_to_csv("sorting_results.csv")
visualize_results(results)
