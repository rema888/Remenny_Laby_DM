import math
def solve_lzw_with_comparison(input_path, max_table_size=4096):
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()

    total_chars = len(text)

    # --- 1. АЛГОРИТМ LZW ---
    alphabet = sorted(list(set(text)))
    dictionary = {char: i for i, char in enumerate(alphabet)}
    dict_size = len(alphabet)
    current_phrase = ""
    compressed_data = []

    for char in text:
        phrase_plus_char = current_phrase + char
        if phrase_plus_char in dictionary:
            current_phrase = phrase_plus_char
        else:
            if current_phrase:
                compressed_data.append(dictionary[current_phrase])
            if dict_size < max_table_size:
                dictionary[phrase_plus_char] = dict_size
                dict_size += 1
            current_phrase = char

    # Не забываем последний фрагмент
    if current_phrase:
        compressed_data.append(dictionary[current_phrase])

    # --- 2. РАСЧЕТ ОБЪЕМОВ В БИТАХ (ДЛЯ КОЭФФИЦИЕНТА K) ---
    # Равномерный код (5 бит на символ)
    size_uncompressed = total_chars * 5  # 81675

    # LZW биты: кол-во кодов * 12 бит
    bits_per_code = math.ceil(math.log2(max_table_size))
    total_lzw_bits = len(compressed_data) * bits_per_code  # 61452

    # Данные Хаффмана из ЛР2 (ОБЪЕМЫ)
    actual_huffman_bits_v1 = 69178
    actual_huffman_bits_v2 = 62122

    # Коэффициенты сжатия (K = сжатый / несжатый)
    k_lzw = total_lzw_bits / size_uncompressed
    k_h1 = actual_huffman_bits_v1 / size_uncompressed
    k_h2 = actual_huffman_bits_v2 / size_uncompressed

    # --- 3. СРАВНЕНИЕ "БИТ НА СИМВОЛ" (КАК ВО 2-М ЗАДАНИИ) ---
    avg_lzw_bits = total_lzw_bits / total_chars
    # Данные из твоей ЛР2 (СРЕДНЯЯ ДЛИНА)
    avg_h1 = 4.2350
    avg_h2 = 3.8004

    # --- ВЫВОД ТАБЛИЦЫ 1: КОЭФФИЦИЕНТ СЖАТИЯ ---
    print("\n" + "=" * 75)
    print(f"{'МЕТОД СЖАТИЯ':<30} | {'ОБЪЕМ (бит)':<15} | {'КОЭФ. СЖАТИЯ (K)':<15}")
    print("-" * 75)
    print(f"{'Равномерный код (5 бит)':<30} | {size_uncompressed:<15} | {1.0000:<15.4f}")
    print(f"{'Хаффман (одиночные)':<30} | {actual_huffman_bits_v1:<15} | {k_h1:<15.4f}")
    print(f"{'Хаффман (пары)':<30} | {actual_huffman_bits_v2:<15} | {k_h2:<15.4f}")
    print(f"{'LZW (словарь 4096)':<30} | {total_lzw_bits:<15} | {k_lzw:<15.4f}")
    print("=" * 75)

    # --- ВЫВОД ТАБЛИЦЫ 2: БИТ НА СИМВОЛ ---
    print(f"\nСРАВНЕНИЕ СРЕДНЕЙ ДЛИНЫ КОДА (бит/символ):")
    print(f"{'Вариант':<30} | {'Бит на символ':<20}")
    print("-" * 55)
    print(f"{'Хаффман (1 символ)':<30} | {avg_h1:<20.4f}")
    print(f"{'Хаффман (пары)':<30} | {avg_h2:<20.4f}")
    print(f"{'LZW':<30} | {avg_lzw_bits:<20.4f}")
    print("-" * 55)

    return total_lzw_bits

lzw_result = solve_lzw_with_comparison('laba4.txt', 4096)