import collections
import json
def generate_stats(input_path, stats_output):
    with open(input_path, 'r') as f:
        text = f.read() # Читаем весь текст из файла в одну строку

    total_chars = len(text)

    # Считаем символы
    char_counts = dict(collections.Counter(text))
    sorted_chars = sorted(char_counts.items(), key=lambda x: x[1], reverse=True)

    # Считаем биграммы
    bigrams = [text[i:i + 2] for i in range(total_chars - 1)]
    bigram_counts = dict(collections.Counter(bigrams))
    sorted_bigrams = sorted(bigram_counts.items(), key=lambda x: x[1], reverse=True)

    # Вывод 5 часто встречающихся символов
    print(f"{'Символ':<10} | {'Кол-во':<10} | {'Частота (%)'}")
    print("-" * 35)
    for char, count in sorted_chars[:5]:
        display_char = f"'{char}'" if char != " " else "'SPACE'"
        freq_percent = (count / total_chars) * 100
        print(f"{display_char:<10} | {count:<10} | {freq_percent:.2f}%")

    # Вывод 5 часто встречающихся биграмм
    print(f"\n{'Пара':<10} | {'Кол-во':<10} | {'Частота (%)'}")
    print("-" * 35)
    total_bigrams = total_chars - 1
    for bg, count in sorted_bigrams[:5]:
        display_bg = f"'{bg.replace(' ', '_')}'"
        freq_percent = (count / total_bigrams) * 100
        print(f"{display_bg:<10} | {count:<10} | {freq_percent:.2f}%")

    # Сохранение полной статистики
    stats_data = {
        "total_chars": total_chars,
        "char_frequencies": char_counts,
        "bigram_frequencies": bigram_counts
    }
    with open(stats_output, 'w') as f_out:
        json.dump(stats_data, f_out, ensure_ascii=False, indent=4)

generate_stats('laba4.txt', 'full_stats.json')