"""
Утилиты для работы с файлами датасета.
"""

import os
import random
from typing import Tuple, Set, Optional


def extract_rev_type_and_number_from_filename(filename: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Извлекает тип отзыва и номер из имени файла.

    Args:
        filename: Имя файла

    Returns:
        Кортеж (rev_type, number) или (None, None) если не удалось извлечь
    """
    # Удаляем расширение .txt
    if filename.endswith('.txt'):
        filename = filename[:-4]

    # Пытаемся извлечь по шаблону {type}_{number}
    if '_' in filename:
        parts = filename.split('_')
        if len(parts) >= 2:
            rev_type = parts[0]
            number = parts[-1] if parts[-1].isdigit() and len(parts[-1]) == 4 else None
            return rev_type, number

    # Альтернативная логика для исходного формата
    # Ищем 'bad' в имени
    if 'bad' in filename.lower():
        # Извлекаем 4 цифры после 'bad'
        import re
        numbers = re.findall(r'\d{4}', filename)
        if numbers:
            return 'bad', numbers[-1]

    return None, None


def generate_unique_filename(existing_names: Set[str], length: int = 4) -> str:
    """
    Генерирует уникальное имя файла.

    Args:
        existing_names: Множество уже использованных имен
        length: Длина числовой части

    Returns:
        Уникальное имя файла
    """
    max_attempts = 10000  # Защита от бесконечного цикла
    for _ in range(max_attempts):
        number = str(random.randint(0, 10 ** length - 1)).zfill(length)
        if number not in existing_names:
            existing_names.add(number)
            return f"{number}.txt"

    raise ValueError(f"Не удалось сгенерировать уникальное имя после {max_attempts} попыток")


def read_file_content(filepath: str) -> str:
    """
    Читает содержимое текстового файла.

    Args:
        filepath: Путь к файлу

    Returns:
        Содержимое файла

    Raises:
        IOError: Если не удалось прочитать файл
        UnicodeDecodeError: Если проблема с кодировкой
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()


def write_file_content(filepath: str, content: str) -> None:
    """
    Записывает содержимое в текстовый файл.

    Args:
        filepath: Путь к файлу
        content: Содержимое для записи
    """
    # Создаем директорию, если ее нет
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)


def find_text_files(directory: str) -> list:
    """
    Находит все текстовые файлы в директории (рекурсивно).

    Args:
        directory: Путь к директории

    Returns:
        Список путей к .txt файлам
    """
    text_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                text_files.append(os.path.join(root, file))
    return text_files