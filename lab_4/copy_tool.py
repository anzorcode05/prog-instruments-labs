import os
import csv


def extract_rev_type_and_number_from_path(path: str) -> tuple[str, str]:
    """
    Извлекает тип отзыва и номер из пути к файлу.

    Args:
        path: Путь к файлу

    Returns:
        Кортеж (rev_type, number)
    """
    # Извлекаем последние 13 символов для анализа
    end_part = os.path.basename(path)[-13:]

    # Проверяем, заканчивается ли на 'bad' (3 символа)
    if end_part[:3] == 'bad':
        rev_type = 'bad'
        # Номер - это 4 цифры перед расширением .txt
        number = end_part[4:8]  # Позиции после '_bad_'
    else:
        # Для других типов берем 4 символа перед номером
        rev_type = end_part[:4]
        number = end_part[5:9]  # Позиции после '_{type}_'

    return rev_type, number


def copy_to_new_directory(path_old: str, path_new: str) -> None:
    """
    Функция копирования исходного датасета в другую директорию.

    Args:
        path_old: Путь к исходной директории
        path_new: Путь к новой директории
    """
    # Создаем новую директорию, если ее нет
    os.makedirs(path_new, exist_ok=True)

    for filename in os.listdir(path_old):
        path = os.path.join(path_old, filename)

        # Пропускаем если не файл или не .txt
        if not (os.path.isfile(path) and filename.endswith('.txt')):
            continue

        try:
            # Извлекаем тип и номер из имени файла
            rev_type, number = extract_rev_type_and_number_from_path(path)

            # Читаем содержимое файла
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Формируем новое имя файла
            new_filename = f"{rev_type}_{number}.txt"
            new_path = os.path.join(path_new, new_filename)

            # Записываем в новый файл
            with open(new_path, 'w', encoding='utf-8') as file:
                file.write(content)

        except (IOError, UnicodeDecodeError) as e:
            print(f"Ошибка при обработке файла {path}: {e}")


def create_new_dir_ann(directory: str, output_csv: str = "data1.csv") -> None:
    """
    Функция создания аннотации для нового датасета.

    Args:
        directory: Путь к директории с файлами
        output_csv: Имя выходного CSV файла
    """
    columns = ("Path1", "Path2", "Class")

    with open(output_csv, "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(columns)

        for filename in os.listdir(directory):
            path = os.path.join(directory, filename)

            if not (os.path.isfile(path) and filename.endswith('.txt')):
                continue

            try:
                # Извлекаем тип и номер из имени файла
                rev_type, number = extract_rev_type_and_number_from_path(path)

                # Формируем новый путь для аннотации
                new_filename = f"{rev_type}_{number}.txt"
                new_path = os.path.join(directory, new_filename)

                # Записываем информацию в CSV
                file_info = (path, new_path, rev_type)
                writer.writerow(file_info)

            except Exception as e:
                print(f"Ошибка при обработке файла {path}: {e}")