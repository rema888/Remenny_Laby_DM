import json
import heapq
import math
def build_huffman(frequencies):
    # Если на вход ничего не пришло, возвращаем пустой словарь
    if not frequencies: return {}
    # Формируем начальные "листья" дерева: [вес, [символ, "пустой_код"]]
    heap = [[weight, [item, ""]] for item, weight in frequencies.items()]
    # Превращаем список в структуру "минимальная куча" (самый легкий элемент всегда сверху)
    heapq.heapify(heap)
    # Пока в куче больше одного узла, продолжаем строить дерево
    while len(heap) > 1:
        # Извлекаем два самых редких (легких) узла
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        # Всем символам из левой ветки дописываем '0' в начало кода, а из правой - '1'
        for pair in lo[1:]: pair[1] = '0' + pair[1]
        for pair in hi[1:]: pair[1] = '1' + pair[1]
        # Объединяем их в новый узел (сумма весов) и кладем обратно в кучу
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    # В куче остался один корень. Превращаем список пар [символ, код] в словарь
    return dict(heap[0][1:])


def encode_text(input_path, codes, output_path):
    with open(input_path, 'r') as f:
        text = f.read()

    # Заменяем каждый символ текста на его код из словаря
    encoded_string = "".join([codes[char] for char in text])

    # Сохраняем как текстовый файл из нулей и единиц
    with open(output_path, 'w') as f_out:
        f_out.write(encoded_string)

    return len(encoded_string)

def run_full_assignment(stats_file, source_text):

    with open(stats_file, 'r') as f:
        data = json.load(f)

    total_n = data["total_chars"]
    char_freqs = data["char_frequencies"]
    bi_freqs = data["bigram_frequencies"]
    total_bi = sum(bi_freqs.values())

    # Коды Хаффмана
    codes_v1 = build_huffman(char_freqs)
    codes_v2 = build_huffman(bi_freqs)

    # Кодирование текста
    actual_bits = encode_text(source_text, codes_v1, 'encoded_huffman.txt')

    # Средняя длина (бит на символ)
    # Для одиночных
    avg_h1 = sum((count / total_n) * len(codes_v1[char]) for char, count in char_freqs.items())
    # Для пар (делим на 2, так как один код на два символа)
    avg_h2 = sum((count / total_bi) * len(codes_v2[bi]) for bi, count in bi_freqs.items()) / 2

    # Энтропия Шеннона
    shannon_h1 = sum(-(c / total_n) * math.log2(c / total_n) for c in char_freqs.values())
    shannon_h2 = sum(-(c / total_bi) * math.log2(c / total_bi) for c in bi_freqs.values()) / 2

    # Равномерный код (по заданию 5 бит)
    uniform_code = 5.0

    print(f"{'ПОКАЗАТЕЛЬ':<25} | {'ЗНАЧЕНИЕ (бит/симв)':<20}")

    print(f"{'Равномерный код':<25} | {uniform_code:<20.4f}")

    print(f"{'Хаффман (один символ)':<25} | {avg_h1:<20.4f}")
    print(f"{'Хаффман (пары символов)':<25} | {avg_h2:<20.4f}")

    print(f"{'Шеннон (один символ)':<25} | {shannon_h1:<20.4f}")
    print(f"{'Шеннон (пары символов)':<25} | {shannon_h2:<20.4f}")

    print(f"\nАнализ эффективности:")
    print(f"Хаффман (1 симв) эффективнее равномерного на: {((1 - avg_h1 / 5) * 100):.2f}%")
    print(f"Хаффман (2 симв) эффективнее равномерного на: {((1 - avg_h2 / 5) * 100):.2f}%")

    print(f"Фактическая длина: {actual_bits} бит")

    # Сохраняем коды в отдельный файл
    huffman_export = {
        "char_codes": codes_v1,
        "bigram_codes": codes_v2
    }

    with open('huffman_codes.json', 'w') as f_codes:
        json.dump(huffman_export, f_codes, ensure_ascii=False, indent=4)

run_full_assignment('full_stats.json', 'laba4.txt')



