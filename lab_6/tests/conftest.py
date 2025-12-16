# tests/conftest.py
import pytest
import tempfile
import os
from datetime import datetime


def pytest_sessionstart(session):
    """Начало сессии - создаем чистый файл"""
    # Создаем пустой файл
    with open("results.txt", "w", encoding="utf-8") as f:
        f.write("ХОД ВЫПОЛНЕНИЯ ТЕСТОВ:\n")
        f.write("-" * 80 + "\n")


def pytest_runtest_logreport(report):
    """Записываем каждый тест в файл"""
    if report.when == 'call':
        with open("results.txt", "a", encoding="utf-8") as f:
            # Форматируем имя теста
            test_name = report.nodeid

            # Получаем иконку статуса
            if report.outcome == 'passed':
                icon = "✅"
                status = "PASSED"
            elif report.outcome == 'failed':
                icon = "❌"
                status = "FAILED"
            elif report.outcome == 'skipped':
                icon = "⏭️"
                status = "SKIPPED"
            else:
                icon = "❓"
                status = report.outcome.upper()

            # Записываем в нужном формате
            f.write(f"{icon} {test_name} {status} ({report.duration:.3f} сек)\n")


def pytest_sessionfinish(session, exitstatus):

    pass


@pytest.fixture
def temp_dir():
    """Фикстура для временной директории"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir