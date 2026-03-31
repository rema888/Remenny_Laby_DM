def analyze_text_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

        print(f"Статистика для файла: {file_path}")
        print(f"Всего символов (включая пробелы): {len(content)}")
        print(f"Количество различных символов: {len(set(content))}")

analyze_text_file('laba4.txt')