#!/usr/bin/env python3
"""
Демонстрационный скрипт для проверки логирования
"""

import logging
from corrected import Calculator, logger, operations_logger, error_logger


def test_logging_levels():
    """Тестирование различных уровней логирования"""
    print("Тестирование уровней логирования...")

    logger.debug("Это DEBUG сообщение - видно только в файле лога")
    logger.info("Это INFO сообщение - видно в консоли и в файле")
    logger.warning("Это WARNING сообщение - важно для внимания")
    logger.error("Это ERROR сообщение - ошибка в работе")

    operations_logger.info("АУДИТ: Тестовая операция выполнена")
    error_logger.error("Тестовая ошибка для проверки лога ошибок")


def test_calculator_operations():
    """Тестирование операций калькулятора с логированием"""
    print("\nТестирование операций калькулятора...")

    calc = Calculator()

    # Установим тестовые значения
    calc.num1 = 10
    calc.num2 = 5

    print(f"Числа: {calc.num1}, {calc.num2}")

    # Тестируем операции
    operations = [
        ("add", "Сложение"),
        ("sub", "Вычитание"),
        ("multi", "Умножение"),
        ("div", "Деление"),
        ("square_exponent", "Квадрат первого числа")
    ]

    for op_code, op_name in operations:
        try:
            result = calc.run_operation(op_code)
            print(f"{op_name}: {result}")
        except Exception as e:
            print(f"Ошибка в {op_name}: {e}")


def view_log_files():
    """Просмотр содержимого лог-файлов"""
    print("\nСодержимое лог-файлов (первые 10 строк):")

    log_files = ['calculator.log', 'calculator_errors.log', 'calculator_audit.log']

    for log_file in log_files:
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                print(f"\n=== {log_file} ===")
                for line in lines[:10]:
                    print(line.strip())
                if len(lines) > 10:
                    print(f"... и ещё {len(lines) - 10} строк")
        except FileNotFoundError:
            print(f"Файл {log_file} не найден")


if __name__ == "__main__":
    print("=" * 60)
    print("ДЕМОНСТРАЦИЯ ЛОГИРОВАНИЯ В КАЛЬКУЛЯТОРЕ")
    print("=" * 60)

    # Тестируем уровни логирования
    test_logging_levels()

    # Тестируем операции калькулятора
    test_calculator_operations()

    # Показываем логи
    view_log_files()

    print("\n" + "=" * 60)
    print("Все тесты завершены. Проверьте файлы логов.")
    print("=" * 60)