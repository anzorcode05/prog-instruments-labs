# tests/conftest.py
import pytest
import tempfile
import os
from datetime import datetime

# Глобальная переменная для хранения результатов
TEST_RESULTS = []


def pytest_sessionstart(session):
    """Выполняется в начале сессии тестирования"""
    # Очищаем старые результаты
    TEST_RESULTS.clear()


def pytest_runtest_logreport(report):
    """Сохраняем результаты каждого теста"""
    if report.when == 'call':  # Только при вызове теста (не setup/teardown)
        TEST_RESULTS.append({
            'nodeid': report.nodeid,
            'outcome': report.outcome,
            'duration': report.duration,
            'message': report.longreprtext if hasattr(report, 'longreprtext') else ''
        })


def pytest_sessionfinish(session, exitstatus):
    """Выполняется после всех тестов - записываем в файл"""
    write_results_to_file()


def write_results_to_file():
    """Записывает результаты в файл results.txt"""
    with open("results.txt", "w", encoding="utf-8") as f:
        f.write("=" * 70 + "\n")
        f.write("РЕЗУЛЬТАТЫ UNIT-ТЕСТОВ\n")
        f.write(f"Время: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")
        f.write("=" * 70 + "\n\n")

        # Статистика
        passed = sum(1 for r in TEST_RESULTS if r['outcome'] == 'passed')
        failed = sum(1 for r in TEST_RESULTS if r['outcome'] == 'failed')
        skipped = sum(1 for r in TEST_RESULTS if r['outcome'] == 'skipped')
        total = len(TEST_RESULTS)

        f.write(f"📊 СТАТИСТИКА:\n")
        f.write(f"   Всего тестов: {total}\n")
        f.write(f"   ✅ Успешно: {passed}\n")
        f.write(f"   ❌ Провалено: {failed}\n")
        f.write(f"   ⏭️  Пропущено: {skipped}\n")
        f.write(f"   📈 Успешных: {passed / total * 100:.1f}%\n")
        f.write("-" * 70 + "\n\n")

        f.write("📋 ДЕТАЛЬНЫЕ РЕЗУЛЬТАТЫ:\n")
        f.write("-" * 70 + "\n")

        for i, result in enumerate(TEST_RESULTS, 1):
            # Получаем имя теста из nodeid
            test_name = result['nodeid'].split("::")[-1]
            module_name = result['nodeid'].split("::")[0].replace("tests/", "")

            # Иконки для статусов
            icons = {
                'passed': '✅',
                'failed': '❌',
                'skipped': '⏭️'
            }
            icon = icons.get(result['outcome'], '❓')

            f.write(f"{i:3d}. {icon} {test_name}\n")
            f.write(f"     Модуль: {module_name}\n")
            f.write(f"     Статус: {result['outcome']}\n")
            f.write(f"     Время: {result['duration']:.3f} сек\n")

            if result['outcome'] == 'failed' and result['message']:
                f.write(f"     Ошибка: {result['message'][:100]}...\n")

            f.write("-" * 40 + "\n")

        f.write("\n" + "=" * 70 + "\n")
        if failed == 0 and skipped == 0:
            f.write("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!\n")
        elif failed == 0:
            f.write("⚠️  Все тесты прошли, но некоторые были пропущены\n")
        else:
            f.write(f"🚨 ЕСТЬ ПРОВАЛЕННЫЕ ТЕСТЫ: {failed}\n")
        f.write("=" * 70 + "\n")


# Фикстуры для тестов
@pytest.fixture
def temp_dir():
    """Создает временную директорию для тестов"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def sample_text_files(temp_dir):
    """Создает тестовые текстовые файлы"""
    files_data = [
        ("good_1234.txt", "Отличный продукт!"),
        ("bad_5678.txt", "Ужасное качество."),
        ("neutral_9999.txt", "Нормально, но есть недостатки."),
        ("custom_file.txt", "Произвольный файл"),
    ]

    file_paths = []
    for filename, content in files_data:
        filepath = os.path.join(temp_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        file_paths.append(filepath)

    return temp_dir, file_paths