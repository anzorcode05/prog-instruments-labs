import csv
import os
import random
from typing import Set


def copy_to_new_dir_with_random_naming(path_old: str, path_new: str,
                                       output_csv: str = "data2.csv") -> None:
    """
    Функция копирования исходного датасета в новую директорию с присваиванием случайного номера.

    Args:
        path_old: Путь к старому датасету
        path_new: Путь к новому расположению датасета
        output_csv: Имя выходного CSV файла
    """
    # Создаем новую директорию, если ее нет
    os.makedirs(path_new, exist_ok=True)

    columns = ("AbsolutePath", "RelativePath", "Class")
    used_numbers: Set[str] = set()

    with open(output_csv, "w", newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        writer.writerow(columns)

        # Рекурсивно обходим все поддиректории
        for root, dirs, files in os.walk(path_old):
            for filename in files:
                if not filename.endswith(".txt"):
                    continue

                path = os.path.join(root, filename)

                try:
                    # Извлекаем тип отзыва из пути
                    # Ищем 'bad' или другие типы в имени файла
                    if 'bad' in filename.lower():
                        rev_type = 'bad'
                    else:
                        # Извлекаем тип из имени файла (первые символы до _)
                        rev_type = filename.split('_')[0]

                    # Генерируем уникальное имя
                    while True:
                        new_number = str(random.randint(0, 9999)).zfill(4)
                        if new_number not in used_numbers:
                            used_numbers.add(new_number)
                            break

                    # Формируем пути
                    new_filename = f"{new_number}.txt"
                    new_file_path = os.path.join(path_new, new_filename)

                    # Копируем содержимое файла
                    with open(path, 'r', encoding='utf-8') as src_file:
                        content = src_file.read()

                    with open(new_file_path, 'w', encoding='utf-8') as dst_file:
                        dst_file.write(content)

                    # Записываем информацию в CSV
                    # Используем абсолютный и относительный пути
                    rel_path = os.path.relpath(new_file_path, start=os.path.dirname(output_csv))
                    file_info = (new_file_path, rel_path, rev_type)
                    writer.writerow(file_info)

                except (IOError, UnicodeDecodeError) as e:
                    print(f"Ошибка при обработке файла {path}: {e}")