import math
def solve_lzw(input_path, max_table_size=4096):
    with open(input_path, 'r') as f:
        text = f.read()

    # Инициализация словаря базовыми символами
    alphabet = sorted(list(set(text)))
    dictionary = {char: i for i, char in enumerate(alphabet)}
    dict_size = len(alphabet)

    current_phrase = ""
    compressed_data = []

    # Алгоритм сжатия
    for char in text:
        phrase_plus_char = current_phrase + char
        if phrase_plus_char in dictionary:
            current_phrase = phrase_plus_char
        else:
            # Выводим код для найденного префикса
            compressed_data.append(dictionary[current_phrase])

            # Добавляем новую фразу в словарь, если есть место
            if dict_size < max_table_size:
                dictionary[phrase_plus_char] = dict_size
                dict_size += 1

            current_phrase = char

    # Не забываем вывести последний код
    if current_phrase:
        compressed_data.append(dictionary[current_phrase])

    # Расчет эффективности
    bits_per_code = math.ceil(math.log2(max_table_size))
    total_lzw_bits = len(compressed_data) * bits_per_code

    total_chars = len(text)
    avg_lzw_bits = total_lzw_bits / total_chars

    print(f"Размер словаря: {dict_size} гнезд (лимит {max_table_size})")
    print(f"Количество кодов на выходе: {len(compressed_data)}")
    print(f"Бит на один код: {bits_per_code}")
    print(f"Средняя длина: {avg_lzw_bits:.4f} бит/символ")
    print("-" * 35)

    return avg_lzw_bits

lzw_result = solve_lzw('laba4.txt', 4096)