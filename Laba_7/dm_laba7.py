import random, math
import heapq
import time

# Генерация графа
def generate_lab_graph(n):
    adj = [[] for _ in range(n)]
    edges = set()

    # Построение ребра
    def add_e(u, v):
        if u != v and (u, v) not in edges:
            w = random.randint(3, 10)
            adj[u].append((v, w))
            adj[v].append((u, w))
            edges.add((u, v)); edges.add((v, u))

    # 1. K5 (0-4) и K4,5 (5-13)
    [add_e(i, j) for i in range(5) for j in range(i+1, 5)]
    [add_e(i, j) for i in range(5, 9) for j in range(9, 14)]

    # 2. Связность (цепочка по случайным индексам)
    nodes = list(range(n))
    random.shuffle(nodes)
    for i in range(n - 1):
        add_e(nodes[i], nodes[i+1])

    # 3. Добор ребер до средней степени sqrt(n)
    target_m = int(n * math.sqrt(n) / 2)
    while len(edges) // 2 < target_m:
        add_e(random.randint(0, n-1), random.randint(0, n-1))

    return adj

# Алгоритм Флойда-Уоршелла (О(n^3))
def floyd_warshall(n, adj):
    # 1. Инициализация матрицы расстояний
    inf = float('inf')
    dist = [[inf] * n for _ in range(n)]

    # Расстояние от вершины до самой себя равно 0
    for i in range(n):
        dist[i][i] = 0

    # Заполняем матрицу существующими ребрами из твоего adj
    for u in range(n):
        for v, weight in adj[u]:
            dist[u][v] = weight

    # 2. Основной цикл алгоритма
    # k - промежуточная вершина, через которую пытаемся улучшить путь
    for k in range(n):
        for i in range(n):
            for j in range(n):
                # Если путь через вершину k короче, чем текущий путь i-j
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    return dist

# Алгоритм Дейкстры (O(m log n)) где m - число рёбер, n - число вершин
def dijkstra(n, adj, start_node):
    distances = [float('inf')] * n
    # 1. Добавляем массив для хранения индексов вершин-предков
    parents = [None] * n
    distances[start_node] = 0
    pq = [(0, start_node)]

    # 2. Добавляем счетчик итераций
    iterations = 0

    while pq:
        current_d, u = heapq.heappop(pq)
        iterations += 1  # Считаем каждое извлечение из очереди

        if current_d > distances[u]:
            continue

        for v, weight in adj[u]:
            distance = current_d + weight

            if distance < distances[v]:
                distances[v] = distance
                # 3. Запоминаем, что кратчайший путь в v лежит через u
                parents[v] = u
                heapq.heappush(pq, (distance, v))

    return distances, parents, iterations

# Функция для восстановления пути
def get_full_path(parents, target):
    path = []
    curr = target
    while curr is not None:
        path.append(curr)
        curr = parents[curr]
    return path[::-1] # Разворачиваем список, чтобы он шел от 0 до target



# --- ЕДИНЫЙ ТЕСТ НА ГРАФЕ n = 1200 ---
n = 1200
graph = generate_lab_graph(n)

print(f"--- АНАЛИЗ ГРАФА (n={n}) ---")

# 1. ПАРАМЕТРЫ
total_degree = sum(len(neighbors) for neighbors in graph)
m_actual = total_degree // 2
print(f"1. ПАРАМЕТРЫ:")
print(f"   Фактическая средняя степень: {total_degree / n:.2f} (ожидалось {math.sqrt(n):.2f})")
print(f"   Общее число ребер (m): {m_actual}")

# 2. ФЛОЙД-УОРШЕЛЛ (Для сравнения сложности)
print(f"\n2. АЛГОРИТМ ФЛОЙДА-УОРШЕЛЛА:")
start_t = time.time()
f_matrix = floyd_warshall(n, graph)
f_time = time.time() - start_t
print(f"   Время выполнения: {f_time:.2f} сек")
print(f"   Теоретическое кол-во итераций (n^3): {n**3}")

# 3. ДЕЙКСТРА И ВОССТАНОВЛЕНИЕ ПУТИ
print(f"\n3. АЛГОРИТМ ДЕЙКСТРЫ:")
start_t = time.time()
d_distances, d_parents, d_iters = dijkstra(n, graph, 0)
d_time = time.time() - start_t

# Расчет теоретической сложности O(m * log2(n))
theory_complexity = int(m_actual * math.log2(n))

# Находим путь до вершины с максимальным номером
target_node = n - 1
path = get_full_path(d_parents, target_node)

print(f"   Время выполнения: {d_time:.4f} сек")
print(f"   Кратчайший путь (0 -> {target_node}):")
# Если путь короткий — выводим целиком, если длинный — сокращаем
if len(path) <= 10:
    print(f"   Маршрут: {' -> '.join(map(str, path))}")
else:
    print(f"   Маршрут: {' -> '.join(map(str, path[:10]))} ... -> {path[-1]}")
print(f"   Вес пути: {d_distances[target_node]}")
print(f"   Фактическое количество итераций: {d_iters}")
print(f"   Теоретическая сложность O(m log n): ~{theory_complexity} операций")

# 4. СРАВНЕНИЕ
print(f"\n--- СРАВНЕНИЕ С АСИМПТОТИКОЙ ---")
print(f"Алгоритм Флойда требует O(n^3) итераций. Для n={n} это {n**3} операций.")
print(f"Алгоритм Дейкстры выполнил всего {d_iters} извлечений из очереди.")