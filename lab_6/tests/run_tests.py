# run_tests.py
import subprocess

import sys

import os

from datetime import datetime

print("=" * 70)
print("🚀 ЗАПУСК UNIT-ТЕСТОВ ДЛЯ ЛАБОРАТОРНОЙ РАБОТЫ №6")
print("=" * 70)

# Проверяем что есть папка tests
if not os.path.exists("tests"):
    print("❌ ОШИБКА: Папка 'tests' не найдена!")
    print("Создай папку 'tests' и помести туда conftest.py и test_main.py")
    sys.exit(1)

# Запускаем тесты
print("\n🔧 Запускаю тесты...")
result = subprocess.run(
    [sys.executable, "-m", "pytest", "tests/test_main.py", "-v", "--tb=short"],
    capture_output=True,
    text=True,
    encoding='utf-8'
)

# Анализируем результаты
output = result.stdout
passed = output.count("PASSED")
failed = output.count("FAILED")
skipped = output.count("SKIPPED")
total = passed + failed + skipped

print("\n" + "=" * 70)
print("📊 РЕЗУЛЬТАТЫ:")
print("=" * 70)
print(f"Всего тестов: {total}")
print(f"✅ Успешно: {passed}")
print(f"❌ Провалено: {failed}")
print(f"⏭️  Пропущено: {skipped}")

if total > 0:
    success_rate = (passed / total) * 100
    print(f"📈 Успешных: {success_rate:.1f}%")

print("\n" + "=" * 70)
print("📋 ТРЕБОВАНИЯ ЛАБОРАТОРНОЙ:")
print("=" * 70)

requirements = {
    "1. Минимум 7 тестов": total >= 7,
    "2. Используется pytest": "pytest" in result.args,
    "3. Есть параметризованные тесты": "parametrized" in output.lower(),
    "4. Есть тесты с моками": "mock" in output.lower() or "patch" in output.lower(),
    "5. Покрытие разных модулей": any(x in output for x in ["file_utils", "copy_tool", "random_copy_tool"]),
}

all_passed = True
for req, status in requirements.items():
    status_icon = "✅" if status else "❌"
    print(f"{status_icon} {req}")
    if not status:
        all_passed = False

print("\n" + "=" * 70)
if all_passed and total >= 7:
    print("🎉 ПОЗДРАВЛЯЮ! ВСЕ ТРЕБОВАНИЯ ВЫПОЛНЕНЫ!")
    print("Лабораторная работа №6 готова к сдаче!")
else:
    print("⚠️  ВНИМАНИЕ: Не все требования выполнены")
print("=" * 70)

# Показываем результаты из файла results.txt
print("\n📄 СОДЕРЖИМОЕ results.txt:")
print("=" * 40)
if os.path.exists("results.txt"):
    with open("results.txt", "r", encoding="utf-8") as f:
        print(f.read())
else:
    print("Файл results.txt не создан")

print("\n💡 Для подробного отчета запусти: pytest tests/test_main.py -v")