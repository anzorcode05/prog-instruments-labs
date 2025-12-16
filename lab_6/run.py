# run_silent.py
import subprocess
import sys
import os


def main():
    """Запускает тесты без вывода в терминал"""

    # Удаляем старый results.txt если есть
    if os.path.exists("results.txt"):
        os.remove("results.txt")

    # Запускаем pytest с перенаправлением вывода в никуда
    subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-q"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # Выводим только одно сообщение
    print("Код выполнен. Результаты тестов в файле results.txt")


if __name__ == "__main__":
    main()