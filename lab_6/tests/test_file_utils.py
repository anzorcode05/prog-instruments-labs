# tests/test_file_utils.py
import pytest
import os
from unittest.mock import patch, mock_open, MagicMock
import random

from file_utils import (
    extract_rev_type_and_number_from_filename,
    generate_unique_filename,
    read_file_content,
    write_file_content,
    find_text_files
)


class TestExtractRevType:
    """Тесты для extract_rev_type_and_number_from_filename"""

    def test_simple_extraction(self):
        """Простые случаи извлечения"""
        # Стандартный формат
        assert extract_rev_type_and_number_from_filename("good_1234.txt") == ("good", "1234")
        assert extract_rev_type_and_number_from_filename("bad_5678.txt") == ("bad", "5678")

        # Без расширения
        assert extract_rev_type_and_number_from_filename("neutral_9999") == ("neutral", "9999")

    def test_bad_format_extraction(self):
        """Формат с 'bad' в названии"""
        assert extract_rev_type_and_number_from_filename("review_bad_1234.txt") == ("bad", "1234")
        assert extract_rev_type_and_number_from_filename("product_bad_9876.txt") == ("bad", "9876")

    def test_invalid_filenames(self):
        """Некорректные имена файлов"""
        assert extract_rev_type_and_number_from_filename("bad.txt") == (None, None)
        assert extract_rev_type_and_number_from_filename("1234.txt") == (None, None)
        assert extract_rev_type_and_number_from_filename("") == (None, None)
        assert extract_rev_type_and_number_from_filename("just_name") == (None, None)

    @pytest.mark.parametrize("filename,expected", [
        ("good_0001.txt", ("good", "0001")),
        ("bad_9999.txt", ("bad", "9999")),
        ("excellent_1234.txt", ("excellent", "1234")),
        ("test_bad_5555.txt", ("bad", "5555")),
        ("file.txt", (None, None)),
        ("no_number.txt", (None, None)),
    ])
    def test_parametrized_extraction(self, filename, expected):
        """Параметризованный тест (ПРОДВИНУТЫЙ ТЕСТ №1)"""
        result = extract_rev_type_and_number_from_filename(filename)
        assert result == expected


class TestFileOperations:
    """Тесты для операций с файлами"""

    def test_read_file_content(self):
        """Тест чтения файла"""
        mock_content = "Содержимое тестового файла\nс двумя строками"
        with patch("builtins.open", mock_open(read_data=mock_content)):
            result = read_file_content("test.txt")
            assert result == mock_content

    def test_write_file_content(self):
        """Тест записи файла"""
        test_content = "Текст для записи в файл"
        mock_file = mock_open()

        with patch("builtins.open", mock_file), \
                patch("os.makedirs") as mock_makedirs:
            write_file_content("/some/dir/file.txt", test_content)

            # Проверяем создание директории
            mock_makedirs.assert_called_once_with("/some/dir", exist_ok=True)
            # Проверяем запись
            mock_file().write.assert_called_once_with(test_content)

    def test_find_text_files(self):
        """Тест поиска текстовых файлов"""
        mock_walk_result = [
            ("/root", ["dir1", "dir2"], ["file1.txt", "file2.jpg", "file3.txt"]),
            ("/root/dir1", [], ["file4.txt", "file5.dat"]),
            ("/root/dir2", ["subdir"], ["file6.txt"]),
            ("/root/dir2/subdir", [], ["file7.txt", "file8.png"]),
        ]

        with patch("os.walk", return_value=mock_walk_result):
            files = find_text_files("/root")

            expected = [
                "/root/file1.txt",
                "/root/file3.txt",
                "/root/dir1/file4.txt",
                "/root/dir2/file6.txt",
                "/root/dir2/subdir/file7.txt",
            ]

            assert sorted(files) == sorted(expected)


class TestUniqueFilename:
    """Тесты для генерации уникальных имен"""

    def test_generate_unique_filename(self):
        """Тест генерации уникального имени"""
        used_names = {"0001", "0002", "0003"}

        # Мокаем random.randint для предсказуемости (ПРОДВИНУТЫЙ ТЕСТ №2)
        with patch("random.randint") as mock_randint:
            # Симулируем: первые два значения уже используются, третье - свободно
            mock_randint.side_effect = [1, 2, 3, 4]

            # Первая генерация - возвращает 0004 (так как 0001-0003 уже заняты)
            result1 = generate_unique_filename(used_names, length=4)
            assert result1 == "0004.txt"
            assert "0004" in used_names

            # Вторая генерация - возвращает следующее свободное
            result2 = generate_unique_filename(used_names, length=4)
            assert result2 == "0005.txt"
            assert "0005" in used_names

    def test_generate_unique_filename_exhaustion(self):
        """Тест исчерпания попыток генерации"""
        # Используем все возможные имена для длины 1 (0-9)
        used_names = set(str(i) for i in range(10))

        with patch("random.randint", return_value=0):  # Всегда возвращает 0
            with pytest.raises(ValueError, match="Не удалось сгенерировать уникальное имя после 10000 попыток"):
                generate_unique_filename(used_names, length=1)