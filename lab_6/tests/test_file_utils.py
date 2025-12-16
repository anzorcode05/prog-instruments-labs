# tests/test_file_utils.py
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, mock_open

from file_utils import (
    extract_rev_type_and_number_from_filename,
    generate_unique_filename,
    read_file_content,
    write_file_content,
    find_text_files
)


# ТЕСТ 1: Базовый тест извлечения
def test_extract_basic():
    """Базовый тест извлечения типа и номера"""
    assert extract_rev_type_and_number_from_filename("good_1234.txt") == ("good", "1234")
    assert extract_rev_type_and_number_from_filename("bad_5678.txt") == ("bad", "5678")


# ТЕСТ 2: Тест без расширения
def test_extract_without_extension():
    """Тест файла без .txt расширения"""
    result = extract_rev_type_and_number_from_filename("test_9999")
    assert result == ("test", "9999")


# ТЕСТ 3: ПАРАМЕТРИЗОВАННЫЙ ТЕСТ (продвинутый №1(внутри 5 тестов(параметров))
@pytest.mark.parametrize("filename,expected_type,expected_number", [
    ("good_0001.txt", "good", "0001"),
    ("bad_9999.txt", "bad", "9999"),
    ("excellent_1234.txt", "excellent", "1234"),
    ("test_5555.txt", "test", "5555"),
    ("invalid.txt", None, None),
])
def test_parametrized_extraction(filename, expected_type, expected_number):
    """Параметризованный тест различных форматов имен"""
    result_type, result_number = extract_rev_type_and_number_from_filename(filename)
    assert result_type == expected_type
    assert result_number == expected_number


# ТЕСТ 4: Тест чтения файла
def test_read_file_content():
    """Тест чтения содержимого файла"""
    mock_content = "Тестовое содержимое файла"
    with patch("builtins.open", mock_open(read_data=mock_content)):
        result = read_file_content("test.txt")
        assert result == mock_content


# ТЕСТ 5: Тест записи файла
def test_write_file_content():
    """Тест записи содержимого в файл"""
    test_content = "Текст для записи"
    mock_file = mock_open()

    with patch("builtins.open", mock_file), \
            patch("os.makedirs") as mock_makedirs:
        write_file_content("/test/dir/file.txt", test_content)
        mock_makedirs.assert_called_once_with("/test/dir", exist_ok=True)
        mock_file().write.assert_called_once_with(test_content)


# ТЕСТ 6: ТЕСТ С МОКОМ RANDOM (продвинутый №2)
def test_generate_unique_filename_with_mock():
    """Тест генерации уникального имени с моком random"""
    used_names = {"0001", "0002"}

    with patch("random.randint") as mock_randint:
        # Мокаем random для предсказуемости
        mock_randint.side_effect = [1, 2, 3]  # 0001 и 0002 заняты, 0003 свободно

        result = generate_unique_filename(used_names, length=4)

        assert result == "0003.txt"
        assert "0003" in used_names
        assert mock_randint.call_count >= 3