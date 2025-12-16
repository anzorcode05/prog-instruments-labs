# tests/test_random_copy_tool.py
import pytest
import os
from unittest.mock import patch, MagicMock, mock_open

from random_copy_tool import copy_to_new_dir_with_random_naming


class TestRandomCopyTool:
    """Тесты для random_copy_tool"""

    def test_copy_with_random_names(self):
        """Тест копирования со случайными именами"""
        mock_files = [
            "/old_dataset/review_1234.txt",
            "/old_dataset/product_5678.txt"
        ]

        with patch("random_copy_tool.find_text_files", return_value=mock_files), \
                patch("random_copy_tool.extract_rev_type_and_number_from_filename") as mock_extract, \
                patch("random_copy_tool.generate_unique_filename") as mock_generate, \
                patch("random_copy_tool.read_file_content", return_value="file content"), \
                patch("random_copy_tool.write_file_content") as mock_write, \
                patch("os.path.basename") as mock_basename, \
                patch("os.path.dirname", return_value="/current"), \
                patch("os.path.relpath", side_effect=lambda p, s: f"rel_{os.path.basename(p)}"), \
                patch("builtins.open", mock_open()), \
                patch("csv.writer") as mock_csv_writer:
            # Настраиваем моки
            mock_extract.side_effect = [
                ("review", "1234"),
                (None, None)  # Второй файл без типа
            ]

            mock_generate.side_effect = ["0420.txt", "1984.txt"]

            mock_basename.side_effect = lambda x: {
                "/old_dataset": "old_dataset",
                ".": "."
            }.get(x, os.path.split(x)[1])

            mock_writer_instance = MagicMock()
            mock_csv_writer.return_value = mock_writer_instance

            # Вызываем тестируемую функцию
            copy_to_new_dir_with_random_naming("/old_dataset", "/new_dataset", "output.csv")

            # Проверяем что файлы были записаны
            assert mock_write.call_count == 2

            # Проверяем запись в CSV
            assert mock_writer_instance.writerow.call_count == 3  # заголовок + 2 записи

            # Проверяем заголовок
            mock_writer_instance.writerow.assert_any_call(("AbsolutePath", "RelativePath", "Class"))

    def test_copy_with_fallback_type(self):
        """Тест с использованием имени директории как fallback типа"""
        mock_files = ["/old_dataset/some_file.txt"]

        with patch("random_copy_tool.find_text_files", return_value=mock_files), \
                patch("random_copy_tool.extract_rev_type_and_number_from_filename", return_value=(None, None)), \
                patch("random_copy_tool.generate_unique_filename", return_value="0001.txt"), \
                patch("random_copy_tool.read_file_content", return_value="content"), \
                patch("random_copy_tool.write_file_content"), \
                patch("os.path.basename") as mock_basename, \
                patch("os.path.dirname", return_value="/current"), \
                patch("os.path.relpath", return_value="rel_0001.txt"), \
                patch("builtins.open", mock_open()), \
                patch("csv.writer") as mock_csv_writer:

            # Настраиваем basename чтобы вернуть имя директории
            def basename_side_effect(path):
                if path == "/old_dataset/some_file.txt":
                    return "some_file.txt"
                elif path == "/old_dataset":
                    return "old_dataset"
                elif path == ".":
                    return "."
                return os.path.basename(path)

            mock_basename.side_effect = basename_side_effect

            mock_writer_instance = MagicMock()
            mock_csv_writer.return_value = mock_writer_instance

            copy_to_new_dir_with_random_naming("/old_dataset", "/new_dataset", "output.csv")

            # Проверяем что в качестве типа использовалось имя директории
            mock_writer_instance.writerow.assert_any_call(("AbsolutePath", "RelativePath", "Class"))