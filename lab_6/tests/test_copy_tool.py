# tests/test_copy_tool.py
import pytest
import csv
import os
from unittest.mock import patch, mock_open, MagicMock, call

from copy_tool import copy_to_new_directory, create_new_dir_ann


class TestCopyToNewDirectory:
    """Тесты для функции copy_to_new_directory"""

    def test_copy_files_success(self):
        """Успешное копирование файлов"""
        mock_files = [
            "/source/good_1234.txt",
            "/source/bad_5678.txt",
            "/source/neutral_9999.txt"
        ]

        mock_content = "Содержимое файла"

        with patch("copy_tool.find_text_files", return_value=mock_files), \
                patch("copy_tool.extract_rev_type_and_number_from_filename") as mock_extract, \
                patch("copy_tool.read_file_content", return_value=mock_content), \
                patch("copy_tool.write_file_content") as mock_write, \
                patch("builtins.print") as mock_print:

            # Настраиваем мок для извлечения данных
            def extract_side_effect(filename):
                if "good_1234" in filename:
                    return "good", "1234"
                elif "bad_5678" in filename:
                    return "bad", "5678"
                elif "neutral_9999" in filename:
                    return "neutral", "9999"
                return None, None

            mock_extract.side_effect = extract_side_effect

            # Вызываем тестируемую функцию
            copy_to_new_directory("/source", "/destination")

            # Проверяем что все файлы были обработаны
            assert mock_write.call_count == 3

            # Проверяем конкретные вызовы
            expected_calls = [
                call("/destination/good_1234.txt", mock_content),
                call("/destination/bad_5678.txt", mock_content),
                call("/destination/neutral_9999.txt", mock_content),
            ]
            mock_write.assert_has_calls(expected_calls, any_order=True)

            # Проверяем что не было сообщений об ошибках
            mock_print.assert_not_called()

    def test_copy_with_invalid_files(self):
        """Копирование с некорректными файлами"""
        mock_files = [
            "/source/good_1234.txt",
            "/source/invalid.txt",  # Некорректное имя
            "/source/bad_5678.txt"
        ]

        with patch("copy_tool.find_text_files", return_value=mock_files), \
                patch("copy_tool.extract_rev_type_and_number_from_filename") as mock_extract, \
                patch("copy_tool.read_file_content"), \
                patch("copy_tool.write_file_content"), \
                patch("builtins.print") as mock_print:

            def extract_side_effect(filename):
                if "good_1234" in filename:
                    return "good", "1234"
                elif "bad_5678" in filename:
                    return "bad", "5678"
                else:
                    return None, None

            mock_extract.side_effect = extract_side_effect

            copy_to_new_directory("/source", "/destination")

            # Проверяем вывод сообщения об ошибке
            mock_print.assert_any_call("Не удалось извлечь тип и номер из файла: invalid.txt")

            # Проверяем что записалось только 2 файла
            assert mock_print.call_count == 1


class TestCreateNewDirAnn:
    """Тесты для функции create_new_dir_ann"""

    def test_create_csv_annotation(self, tmp_path):
        """Тест создания CSV аннотации"""
        # Создаем временный CSV файл
        csv_file = tmp_path / "annotation.csv"

        mock_files = [
            "/dataset/good_0001.txt",
            "/dataset/bad_1234.txt",
            "/dataset/neutral_9999.txt"
        ]

        with patch("copy_tool.find_text_files", return_value=mock_files), \
                patch("copy_tool.extract_rev_type_and_number_from_filename") as mock_extract:
            mock_extract.side_effect = [
                ("good", "0001"),
                ("bad", "1234"),
                ("neutral", "9999")
            ]

            # Вызываем функцию
            create_new_dir_ann("/dataset", str(csv_file))

            # Проверяем созданный файл
            assert csv_file.exists()

            # Читаем и проверяем содержимое
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=';')
                rows = list(reader)

                # Проверяем заголовок
                assert rows[0] == ["OriginalPath", "NewPath", "Class"]

                # Проверяем данные
                assert rows[1] == ["/dataset/good_0001.txt", "/dataset/good_0001.txt", "good"]
                assert rows[2] == ["/dataset/bad_1234.txt", "/dataset/bad_1234.txt", "bad"]
                assert rows[3] == ["/dataset/neutral_9999.txt", "/dataset/neutral_9999.txt", "neutral"]