# tests/test_copy_tool.py
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, mock_open

from copy_tool import copy_to_new_directory, create_new_dir_ann


# ТЕСТ 7: Тест copy_to_new_directory с моками
def test_copy_to_new_directory_mock():
    """Тест функции копирования файлов с использованием моков"""
    mock_files = ["/source/good_1234.txt", "/source/bad_5678.txt"]

    with patch("copy_tool.find_text_files", return_value=mock_files), \
            patch("copy_tool.extract_rev_type_and_number_from_filename") as mock_extract, \
            patch("copy_tool.read_file_content", return_value="content"), \
            patch("copy_tool.write_file_content") as mock_write:

        # Настраиваем мок для извлечения
        def extract_side_effect(filename):
            if "good_1234" in filename:
                return "good", "1234"
            elif "bad_5678" in filename:
                return "bad", "5678"
            return None, None

        mock_extract.side_effect = extract_side_effect

        # Вызываем тестируемую функцию
        copy_to_new_directory("/source", "/destination")

        # Проверяем что оба файла были записаны
        assert mock_write.call_count == 2


# ТЕСТ 8: Тест создания CSV аннотации
def test_create_new_dir_ann_simple():
    """Тест создания CSV файла с аннотациями"""
    mock_files = ["/dataset/file1.txt", "/dataset/file2.txt"]

    with patch("copy_tool.find_text_files", return_value=mock_files), \
            patch("copy_tool.extract_rev_type_and_number_from_filename", return_value=("test", "0001")), \
            patch("builtins.open", mock_open()) as mock_file:
        # Вызываем функцию
        create_new_dir_ann("/dataset", "annotation.csv")

        # Проверяем что файл был открыт для записи
        assert mock_file.called