import os
import csv
from file_utils import (
    extract_rev_type_and_number_from_filename,
    read_file_content,
    write_file_content,
    find_text_files
)


def copy_to_new_directory(path_old: str, path_new: str) -> None:
    """
    Функция копирования исходного датасета в другую директорию.

    Args:
        path_old: Путь к исходной директории
        path_new: Путь к новой директории
    """
    for filepath in find_text_files(path_old):
        try:
            filename = os.path.basename(filepath)
            rev_type, number = extract_rev_type_and_number_from_filename(filename)

            if rev_type and number:
                # Читаем и записываем файл
                content = read_file_content(filepath)
                new_filename = f"{rev_type}_{number}.txt"
                new_path = os.path.join(path_new, new_filename)
                write_file_content(new_path, content)
            else:
                print(f"Не удалось извлечь тип и номер из файла: {filename}")

        except Exception as e:
            print(f"Ошибка при обработке файла {filepath}: {e}")


def create_new_dir_ann(directory: str, output_csv: str = "data1.csv") -> None:
    """
    Функция создания аннотации для нового датасета.

    Args:
        directory: Путь к директории с файлами
        output_csv: Имя выходного CSV файла
    """
    columns = ("OriginalPath", "NewPath", "Class")

    with open(output_csv, "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(columns)

        for filepath in find_text_files(directory):
            try:
                filename = os.path.basename(filepath)
                rev_type, number = extract_rev_type_and_number_from_filename(filename)

                if rev_type and number:
                    new_filename = f"{rev_type}_{number}.txt"
                    new_path = os.path.join(directory, new_filename)
                    file_info = (filepath, new_path, rev_type)
                    writer.writerow(file_info)
                else:
                    print(f"Не удалось извлечь тип и номер из файла: {filename}")

            except Exception as e:
                print(f"Ошибка при обработке файла {filepath}: {e}")