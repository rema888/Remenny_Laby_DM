from collections import Counter

def count_distinct_words(source_word: str, k: int) -> int:

    freq = Counter(source_word)
    all_words = set()

    def enumeration(current: str, freq_left: dict):
        # Если набрали нужную длину — сохраняем
        if len(current) == k:
            all_words.add(current)
            return

        # Пробуем каждую букву, которая ещё доступна
        for letter in freq_left:
            if freq_left[letter] > 0:
                # Используем букву
                freq_left[letter] -= 1
                enumeration(current + letter, freq_left)
                # Возвращаем обратно
                freq_left[letter] += 1

    # Запускаем перебор
    enumeration("", freq)
    return len(all_words)

print("Количество различных слов длины 6:", count_distinct_words("ЧЕРЕСПОЛОСИЦА", 6))