# tests/test_random_copy_tool.py
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, MagicMock, mock_open

from random_copy_tool import copy_to_new_dir_with_random_naming


# ТЕСТ 9: Тест с комплексными моками
def test_copy_with_random_names():
    """Тест копирования со случайными именами с использованием моков"""
    mock_files = ["/old_dataset/review_1234.txt"]

    with patch("random_copy_tool.find_text_files", return_value=mock_files), \
            patch("random_copy_tool.extract_rev_type_and_number_from_filename", return_value=("review", "1234")), \
            patch("random_copy_tool.generate_unique_filename", return_value="0420.txt"), \
            patch("random_copy_tool.read_file_content", return_value="file content"), \
            patch("random_copy_tool.write_file_content"), \
            patch("os.path.basename", return_value="review_1234.txt"), \
            patch("os.path.dirname", return_value="/current"), \
            patch("os.path.relpath", return_value="rel_0420.txt"), \
            patch("builtins.open", mock_open()), \
            patch("csv.writer") as mock_csv_writer:
        mock_writer_instance = MagicMock()
        mock_csv_writer.return_value = mock_writer_instance

        # Вызываем тестируемую функцию
        copy_to_new_dir_with_random_naming("/old_dataset", "/new_dataset", "output.csv")

        # Проверяем что CSV writer был вызван
        assert mock_writer_instance.writerow.called


# ТЕСТ 10: Простой тест импорта и наличия функции
def test_random_copy_tool_import():
    """Тест что модуль импортируется и функция существует"""
    # Просто проверяем что функция существует и может быть вызвана
    assert hasattr(copy_to_new_dir_with_random_naming, '__call__')
    assert True  # Если дошли сюда - импорт успешен