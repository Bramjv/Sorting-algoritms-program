import random
import time
import csv
import matplotlib.pyplot as plt
import heapq


# Funkcja do generowania danych
def generate_data_integer(size, data_type, order="random"):
    data = [random.randint(0, 1000) for _ in range(size)]

    if order == "sorted":
        data.sort()
    elif order == "reverse":
        data.sort(reverse=True)
    elif order == "partially_sorted":
        partially_sorted_size = size // 2
        data[:partially_sorted_size] = sorted(data[:partially_sorted_size])

    return data


def generate_data_float(size, data_type, order="random"):
    data = [random.uniform(0, 1000) for _ in range(size)]

    if order == "sorted":
        data.sort()
    elif order == "reverse":
        data.sort(reverse=True)
    elif order == "partially_sorted":
        partially_sorted_size = size // 2
        data[:partially_sorted_size] = sorted(data[:partially_sorted_size])

    return data


# Implementacja Quick Sort
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[len(arr) // 2]
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


# Implementacja Tim Sort (wbudowany w Pythonie)
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


# Implementacja Radix Sort
def radix_sort(arr):
    max_num = max(arr)
    exp = 1
    while max_num // exp > 0:
        counting_sort_radix(arr, exp)
        exp *= 10
    return arr


def counting_sort_radix(arr, exp):
    output = [0] * len(arr)
    count = [0] * 10

    # Liczymy wystąpienia dla danego cyfrowego miejsca
    for num in arr:
        index = num // exp
        count[index % 10] += 1

    # Przekształcamy count do pozycji
    for i in range(1, 10):
        count[i] += count[i - 1]

    # Budujemy wynik
    i = len(arr) - 1
    while i >= 0:
        num = arr[i]
        index = num // exp
        output[count[index % 10] - 1] = num
        count[index % 10] -= 1
        i -= 1

    # Kopiujemy posortowane elementy z powrotem
    for i in range(len(arr)):
        arr[i] = output[i]


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
    min_value = 100000
    max_value = 10000000
    data_sizes = [random.randint(min_value, max_value) for _ in range(2)]
    data_characteristics = ["random", "sorted", "reverse", "partially_sorted"]
    sort_algorithms = {
        "Quick Sort": quick_sort,
        "Merge Sort": merge_sort,
        "Tim Sort": tim_sort,
        "Bucket Sort": bucket_sort,
        "Radix Sort": radix_sort,
        "Heap Sort": heap_sort
    }

    results = []

    with open(output_file, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Algorithm", "Data Size", "Data Characteristic", "Time (s)", "Data type(integer/float)"])

        for size in data_sizes:
            for characteristic in data_characteristics:
                for algo_name, algo_func in sort_algorithms.items():
                    data = generate_data_float(size, data_type = "float", characteristic)
                    time_taken = measure_sort_time(algo_func, data)
                    writer.writerow([algo_name, size, characteristic, time_taken, data_type])
                    results.append((algo_name, size, characteristic, time_taken, data_type))
                    print(
                        f"Algorytm: {algo_name}, Rozmiar: {size}, Charakterystyka: {characteristic}, Czas: {time_taken:.6f} sekund, Typ danych: {data_type}")

    return results


# Funkcja do wizualizacji wyników
def visualize_results(results):
    algorithms = list(set(result[0] for result in results))
    data_sizes = sorted(list(set(result[1] for result in results)))
    characteristics = list(set(result[2] for result in results))

    for characteristic in characteristics:
        plt.figure(figsize=(10, 6))
        for algo in algorithms:
            times = [
                result[3] for result in results if result[0] == algo and result[2] == characteristic
            ]
            plt.plot(data_sizes, times, marker='o', label=algo)

        plt.title(f"Czas sortowania dla danych: {characteristic}")
        plt.xlabel("Rozmiar danych")
        plt.ylabel("Czas (s)")
        plt.legend()
        plt.grid()
        plt.show()


# Uruchomienie testów, zapisanie wyników i wizualizacja
results = run_tests_and_save_to_csv("sorting_results.csv")
