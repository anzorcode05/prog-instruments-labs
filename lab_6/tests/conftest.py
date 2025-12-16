# tests/conftest.py
import pytest
import tempfile
import os
from datetime import datetime


def pytest_sessionstart(session):
    """Создаем файл результатов в начале"""
    with open("results.txt", "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("РЕЗУЛЬТАТЫ UNIT-ТЕСТОВ\n")
        f.write(f"Время: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")
        f.write("Запуск тестов...\n")


def pytest_sessionfinish(session, exitstatus):
    """Добавляем итоги в конец файла"""
    with open("results.txt", "a", encoding="utf-8") as f:
        f.write("\n" + "=" * 60 + "\n")
        f.write("ИТОГИ:\n")
        f.write(f"Всего тестов: {session.testscollected or 0}\n")
        f.write(
            f"✅ Успешно: {(session.testscollected or 0) - (session.testsfailed or 0) - (session.testsskipped or 0)}\n")
        f.write(f"❌ Провалено: {session.testsfailed or 0}\n")
        f.write(f"⏭️  Пропущено: {session.testsskipped or 0}\n")
        f.write("=" * 60 + "\n")

        if (session.testsfailed or 0) == 0 and (session.testscollected or 0) >= 10:
            f.write("🎉 ВСЕ 10+ ТЕСТОВ ПРОЙДЕНЫ! ТРЕБОВАНИЯ ВЫПОЛНЕНЫ!\n")
        f.write("=" * 60 + "\n")


@pytest.fixture
def temp_dir():
    """Временная директория для тестов"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir