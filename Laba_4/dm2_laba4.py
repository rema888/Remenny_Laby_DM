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
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()
    # Заменяем каждый символ текста на его код из словаря
    encoded_string = "".join([codes[char] for char in text])
    # Сохраняем как текстовый файл из нулей и единиц
    with open(output_path, 'w') as f_out:
        f_out.write(encoded_string)
    return len(encoded_string)

def encode_text_pairs(input_path, codes, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()
    # Если текст нечетной длины, добавим пробел в конец для формирования последней пары
    if len(text) % 2 != 0:
        text += " "
    encoded_list = []
    # Идем по тексту с шагом 2
    for i in range(0, len(text), 2):
        pair = text[i:i+2]
        # Берем код из словаря для пары
        if pair in codes:
            encoded_list.append(codes[pair])
    encoded_string = "".join(encoded_list)
    with open(output_path, 'w') as f_out:
        f_out.write(encoded_string)
    return len(encoded_string)

def run_full_assignment(stats_file, source_text):
    with open(stats_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    total_n = data["total_chars"]
    char_freqs = data["char_frequencies"]
    bi_freqs = data["bigram_frequencies"]
    total_bi = sum(bi_freqs.values())

    # Коды Хаффмана
    codes_v1 = build_huffman(char_freqs)
    codes_v2 = build_huffman(bi_freqs)

    # Кодирование текста (получаем фактическое количество бит)
    actual_bits = encode_text(source_text, codes_v1, 'encoded_huffman.txt')
    actual_bits_v2 = encode_text_pairs(source_text, codes_v2, 'encoded_huffman_pairs.txt')

    # Средняя длина (бит на символ)
    # Для одиночных
    avg_h1 = sum((count / total_n) * len(codes_v1[char]) for char, count in char_freqs.items())
    # Для пар (делим на 2, так как один код на два символа)
    avg_h2 = sum((count / total_bi) * len(codes_v2[bi]) for bi, count in bi_freqs.items()) / 2

    # Энтропия Шеннона (количество бит на символ)
    shannon_h1 = sum(-(c / total_n) * math.log2(c / total_n) for c in char_freqs.values())
    shannon_h2 = sum(-(c / total_bi) * math.log2(c / total_bi) for c in bi_freqs.values()) / 2

    # Равномерный код (по заданию 5 бит) - это размер несжатого текста
    size_uncompressed = total_n * 5

    # Вычисляем коэффициент сжатия K = размер сжатого / размер несжатого
    k1 = actual_bits / size_uncompressed
    k2 = actual_bits_v2 / size_uncompressed

    print("\n" + "="*70)
    print(f"{'МЕТОД':<30} | {'ОБЪЕМ (бит)':<15} | {'КОЭФ. СЖАТИЯ (K)':<15}")
    print("-" * 70)
    print(f"{'Равномерный код (5 бит)':<30} | {size_uncompressed:<15} | {1.0000:<15.4f}")
    print(f"{'Хаффман (1 символ)':<30} | {actual_bits:<15} | {k1:<15.4f}")
    print(f"{'Хаффман (пары)':<30} | {actual_bits_v2:<15} | {k2:<15.4f}")
    print("="*70)

    print(f"\nСРАВНЕНИЕ С ЭНТРОПИЕЙ ШЕННОНА (бит на символ):")
    print(f"{'Вариант':<25} | {'Хаффман (Lcp)':<15} | {'Шеннон (H)':<15}")
    print("-" * 60)
    print(f"{'Одиночные символы':<25} | {avg_h1:<15.4f} | {shannon_h1:<15.4f}")
    print(f"{'Пары символов':<25} | {avg_h2:<15.4f} | {shannon_h2:<15.4f}")

    # Сохраняем коды в отдельный файл
    huffman_export = {
        "char_codes": codes_v1,
        "bigram_codes": codes_v2
    }

    with open('huffman_codes.json', 'w', encoding='utf-8') as f_codes:
        json.dump(huffman_export, f_codes, ensure_ascii=False, indent=4)

run_full_assignment('full_stats.json', 'laba4.txt')