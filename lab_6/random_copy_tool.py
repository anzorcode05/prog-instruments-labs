import csv
import os
from file_utils import (
    extract_rev_type_and_number_from_filename,
    read_file_content,
    write_file_content,
    find_text_files,
    generate_unique_filename
)


def copy_to_new_dir_with_random_naming(path_old: str, path_new: str,
                                       output_csv: str = "data2.csv") -> None:
    """
    Функция копирования исходного датасета в новую директорию с присваиванием случайного номера.

    Args:
        path_old: Путь к старому датасету
        path_new: Путь к новому расположению датасета
        output_csv: Имя выходного CSV файла
    """
    columns = ("AbsolutePath", "RelativePath", "Class")
    used_names = set()

    with open(output_csv, "w", newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        writer.writerow(columns)

        for filepath in find_text_files(path_old):
            try:
                filename = os.path.basename(filepath)

                # Извлекаем тип отзыва
                rev_type, _ = extract_rev_type_and_number_from_filename(filename)
                if not rev_type:
                    # Если не удалось извлечь, используем имя родительской директории
                    rev_type = os.path.basename(os.path.dirname(filepath))
                    if not rev_type or rev_type == '.':
                        rev_type = 'unknown'

                # Генерируем уникальное имя
                new_filename = generate_unique_filename(used_names)
                new_file_path = os.path.join(path_new, new_filename)

                # Копируем файл
                content = read_file_content(filepath)
                write_file_content(new_file_path, content)

                # Записываем информацию в CSV
                rel_path = os.path.relpath(new_file_path, start=os.path.dirname(output_csv))
                file_info = (new_file_path, rel_path, rev_type)
                writer.writerow(file_info)

            except Exception as e:
                print(f"Ошибка при обработке файла {filepath}: {e}")