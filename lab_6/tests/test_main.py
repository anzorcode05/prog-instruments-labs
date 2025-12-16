# tests/test_main.py
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import csv
import tempfile
from unittest.mock import patch, mock_open, MagicMock

# Импортируем ВСЕ функции которые будем тестировать
from file_utils import (
    extract_rev_type_and_number_from_filename,
    generate_unique_filename,
    read_file_content,
    write_file_content,
    find_text_files
)
from copy_tool import copy_to_new_directory, create_new_dir_ann
from random_copy_tool import copy_to_new_dir_with_random_naming


# ==================== ТЕСТ 1-4: БАЗОВЫЕ ТЕСТЫ ====================

def test_1_extract_basic():
    """1. Базовый тест извлечения типа и номера"""
    result = extract_rev_type_and_number_from_filename("good_1234.txt")
    assert result == ("good", "1234")

    result = extract_rev_type_and_number_from_filename("bad_5678.txt")
    assert result == ("bad", "5678")


def test_2_extract_no_extension():
    """2. Тест файла без расширения .txt"""
    result = extract_rev_type_and_number_from_filename("test_9999")
    assert result == ("test", "9999")


def test_3_read_file_content():
    """3. Тест чтения файла"""
    mock_content = "Содержимое файла для теста"
    with patch("builtins.open", mock_open(read_data=mock_content)):
        result = read_file_content("test.txt")
        assert result == mock_content


def test_4_write_file_content():
    """4. Тест записи файла"""
    test_content = "Текст для записи"
    mock_file = mock_open()

    with patch("builtins.open", mock_file), \
            patch("os.makedirs") as mock_makedirs:
        write_file_content("/test/dir/file.txt", test_content)
        mock_makedirs.assert_called_once_with("/test/dir", exist_ok=True)
        mock_file().write.assert_called_once_with(test_content)


# ==================== ТЕСТ 5-6: ПРОДВИНУТЫЕ ТЕСТЫ ====================

@pytest.mark.parametrize("filename,expected_type,expected_number", [
    ("good_0001.txt", "good", "0001"),
    ("bad_9999.txt", "bad", "9999"),
    ("excellent_1234.txt", "excellent", "1234"),
    ("test_5555.txt", "test", "5555"),
    ("invalid.txt", None, None),
])
def test_5_parametrized_extraction(filename, expected_type, expected_number):
    """5. ПАРАМЕТРИЗОВАННЫЙ ТЕСТ (продвинутый №1)"""
    result_type, result_number = extract_rev_type_and_number_from_filename(filename)
    assert result_type == expected_type
    assert result_number == expected_number


def test_6_generate_unique_filename_with_mock():
    """6. ТЕСТ С МОКОМ RANDOM (продвинутый №2)"""
    used_names = {"0001", "0002"}

    with patch("random.randint") as mock_randint:
        # Мокаем random чтобы возвращал предсказуемые значения
        mock_randint.side_effect = [1, 2, 3]  # 0001, 0002 уже заняты, 0003 свободно

        result = generate_unique_filename(used_names, length=4)

        assert result == "0003.txt"
        assert "0003" in used_names
        assert mock_randint.call_count >= 3


# ==================== ТЕСТ 7-10: ДОПОЛНИТЕЛЬНЫЕ ТЕСТЫ ====================

def test_7_find_text_files():
    """7. Тест поиска текстовых файлов"""
    mock_walk_result = [
        ("/test", ["subdir"], ["file1.txt", "file2.jpg"]),
        ("/test/subdir", [], ["file3.txt"]),
    ]

    with patch("os.walk", return_value=mock_walk_result):
        files = find_text_files("/test")

        # Нормализуем пути для кроссплатформенности
        normalized_files = [os.path.normpath(f) for f in files]

        assert len(normalized_files) == 2  # file1.txt и file3.txt
        assert any("file1.txt" in f for f in normalized_files)
        assert any("file3.txt" in f for f in normalized_files)


def test_8_copy_to_new_directory_mock():
    """8. Тест функции copy_to_new_directory с моками"""
    with patch("copy_tool.find_text_files", return_value=["/src/file.txt"]), \
            patch("copy_tool.extract_rev_type_and_number_from_filename", return_value=("good", "1234")), \
            patch("copy_tool.read_file_content", return_value="content"), \
            patch("copy_tool.write_file_content") as mock_write:
        copy_to_new_directory("/src", "/dst")

        # Проверяем что была попытка записать файл
        assert mock_write.called


def test_9_create_new_dir_ann_simple():
    """9. Тест создания CSV аннотации"""
    with patch("copy_tool.find_text_files", return_value=[]), \
            patch("builtins.open", mock_open()):
        # Просто проверяем что функция не падает
        create_new_dir_ann("/test", "output.csv")
        assert True


def test_10_random_copy_tool_import():
    """10. Тест импорта и наличия функции"""
    # Проверяем что функция существует
    assert hasattr(copy_to_new_dir_with_random_naming, '__call__')

    # Проверяем базовый вызов с моками
    with patch("random_copy_tool.find_text_files", return_value=[]), \
            patch("random_copy_tool.extract_rev_type_and_number_from_filename"), \
            patch("random_copy_tool.generate_unique_filename"), \
            patch("random_copy_tool.read_file_content"), \
            patch("random_copy_tool.write_file_content"), \
            patch("os.path.basename"), \
            patch("os.path.dirname"), \
            patch("os.path.relpath"), \
            patch("builtins.open", mock_open()), \
            patch("csv.writer"):
        # Проверяем что функция вызывается без ошибок
        copy_to_new_dir_with_random_naming("/old", "/new", "test.csv")
        assert True