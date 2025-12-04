# This is like making a package.lock file for npm package.
# Yes, I should be making it.
__author__ = "Nitkarsh Chourasia"
__version__ = "0.0.0"
__license__ = "MIT"

import json
import logging
import logging.config
from gtts import gTTS
from pygame import mixer, time
from io import BytesIO
from pprint import pprint
import sys
import os


def setup_logging():
    config_path = 'logging_config.json'

    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            logging.config.dictConfig(config)
            logger = logging.getLogger('calculator')
            logger.info("Логирование успешно настроено из файла %s", config_path)
            return logger
        except Exception as e:
            print(f"Ошибка загрузки конфига логирования: {e}. Используется базовая конфигурация.")

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('calculator.log', encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    logger = logging.getLogger('calculator')
    logger.info("Логирование настроено с базовой конфигурацией")
    return logger


logger = setup_logging()
operations_logger = logging.getLogger('calculator.operations')
error_logger = logging.getLogger('calculator.errors')


class Calculator:
    def __init__(self):
        logger.debug("Инициализация калькулятора")
        self.num1 = None
        self.num2 = None
        self.name = None
        self.gtts_object = None
        self.take_inputs()

    def add(self):
        try:
            result = self.num1 + self.num2
            operations_logger.info("ADDITION: %.2f + %.2f = %.2f", self.num1, self.num2, result)
            logger.debug("Операция сложения выполнена успешно")
            return result
        except Exception as e:
            error_logger.error("Ошибка в операции сложения: %s", e, exc_info=True)
            raise

    def sub(self):
        try:
            result = self.num1 - self.num2
            operations_logger.info("SUBTRACTION: %.2f - %.2f = %.2f", self.num1, self.num2, result)
            logger.debug("Операция вычитания выполнена успешно")
            return result
        except Exception as e:
            error_logger.error("Ошибка в операции вычитания: %s", e, exc_info=True)
            raise

    def multi(self):
        try:
            result = self.num1 * self.num2
            operations_logger.info("MULTIPLICATION: %.2f * %.2f = %.2f", self.num1, self.num2, result)
            logger.debug("Операция умножения выполнена успешно")
            return result
        except Exception as e:
            error_logger.error("Ошибка в операции умножения: %s", e, exc_info=True)
            raise

    def div(self):
        try:
            if self.num2 == 0:
                error_logger.error("Попытка деления на ноль: %.2f / %.2f", self.num1, self.num2)
                raise ZeroDivisionError("Деление на ноль невозможно")

            result = self.num1 / self.num2
            operations_logger.info("DIVISION: %.2f / %.2f = %.2f", self.num1, self.num2, result)
            logger.debug("Операция деления выполнена успешно")
            return result
        except ZeroDivisionError as e:
            error_logger.critical("КРИТИЧЕСКАЯ ОШИБКА: Деление на ноль", exc_info=True)
            raise
        except Exception as e:
            error_logger.error("Ошибка в операции деления: %s", e, exc_info=True)
            raise

    def power(self):
        try:
            result = self.num1 ** self.num2
            operations_logger.info("POWER: %.2f ^ %.2f = %.2f", self.num1, self.num2, result)
            logger.debug("Операция возведения в степень выполнена успешно")
            return result
        except Exception as e:
            error_logger.error("Ошибка в операции возведения в степень: %s", e, exc_info=True)
            raise

    def root(self):
        try:
            if self.num2 == 0:
                error_logger.error("Попытка извлечения корня нулевой степени: %.2f ^ (1/%.2f)", self.num1, self.num2)
                raise ValueError("Невозможно извлечь корень нулевой степени")

            result = self.num1 ** (1 / self.num2)
            operations_logger.info("ROOT: %.2f-th root of %.2f = %.2f", self.num2, self.num1, result)
            logger.debug("Операция извлечения корня выполнена успешно")
            return result
        except Exception as e:
            error_logger.error("Ошибка в операции извлечения корня: %s", e, exc_info=True)
            raise

    def remainder(self):
        try:
            if self.num2 == 0:
                error_logger.error("Попытка вычисления остатка от деления на ноль: %.2f %% %.2f", self.num1, self.num2)
                raise ZeroDivisionError("Деление на ноль невозможно")

            result = self.num1 % self.num2
            operations_logger.info("REMAINDER: %.2f %% %.2f = %.2f", self.num1, self.num2, result)
            logger.debug("Операция вычисления остатка выполнена успешно")
            return result
        except Exception as e:
            error_logger.error("Ошибка в операции вычисления остатка: %s", e, exc_info=True)
            raise

    def cube_root(self):
        try:
            result = self.num1 ** (1 / 3)
            operations_logger.info("CUBE_ROOT: cube root of %.2f = %.2f", self.num1, result)
            logger.debug("Операция извлечения кубического корня выполнена успешно")
            return result
        except Exception as e:
            error_logger.error("Ошибка в операции извлечения кубического корня: %s", e, exc_info=True)
            raise

    def cube_exponent(self):
        try:
            result = self.num1 ** 3
            operations_logger.info("CUBE: %.2f ^ 3 = %.2f", self.num1, result)
            logger.debug("Операция возведения в куб выполнена успешно")
            return result
        except Exception as e:
            error_logger.error("Ошибка в операции возведения в куб: %s", e, exc_info=True)
            raise

    def square_root(self):
        try:
            if self.num1 < 0:
                error_logger.error("Попытка извлечения квадратного корня из отрицательного числа: %.2f", self.num1)
                raise ValueError("Невозможно извлечь квадратный корень из отрицательного числа")

            result = self.num1 ** (1 / 2)
            operations_logger.info("SQUARE_ROOT: sqrt(%.2f) = %.2f", self.num1, result)
            logger.debug("Операция извлечения квадратного корня выполнена успешно")
            return result
        except Exception as e:
            error_logger.error("Ошибка в операции извлечения квадратного корня: %s", e, exc_info=True)
            raise

    def square_exponent(self):
        try:
            result = self.num1 ** 2
            operations_logger.info("SQUARE: %.2f ^ 2 = %.2f", self.num1, result)
            logger.debug("Операция возведения в квадрат выполнена успешно")
            return result
        except Exception as e:
            error_logger.error("Ошибка в операции возведения в квадрат: %s", e, exc_info=True)
            raise

    def calculate_factorial(self):
        try:
            if self.num < 0:
                error_logger.error("Попытка вычисления факториала отрицательного числа: %d", self.num)
                raise ValueError("Факториал определен только для неотрицательных чисел")

            result = 1
            for i in range(1, self.num + 1):
                result = result * i

            operations_logger.info("FACTORIAL: %d! = %d", self.num, result)
            logger.debug("Вычисление факториала выполнено успешно")
            return result
        except Exception as e:
            error_logger.error("Ошибка при вычислении факториала: %s", e, exc_info=True)
            raise

    def greeting(self):
        try:
            logger.info("Запуск приветствия пользователя")
            text_to_audio = "Welcome To The Calculator"
            self.gtts_object = gTTS(
                text=text_to_audio, lang="en", tld="co.in", slow=False
            )
            tts = self.gtts_object
            fp = BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            mixer.init()
            mixer.music.load(fp)
            mixer.music.play()

            logger.debug("Аудио приветствие воспроизводится")
            while mixer.music.get_busy():
                time.Clock().tick(10)

            logger.info("Приветствие завершено")
        except Exception as e:
            error_logger.error("Ошибка при воспроизведении аудио-приветствия: %s", e, exc_info=True)
            logger.warning("Аудио приветствие не воспроизведено, продолжение работы")

    def user_name(self):
        try:
            logger.info("Запрос имени пользователя")
            self.name = input("Please enter your good name: ")

            if not self.name or self.name.strip() == "":
                logger.warning("Пользователь ввел пустое имя")
                self.name = "Guest"

            logger.info("Пользователь представился как: %s", self.name)

            text_to_audio = f"{self.name}"
            self.gtts_object = gTTS(
                text=text_to_audio, lang="en", tld="co.in", slow=False
            )
            tts = self.gtts_object
            fp = BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            mixer.init()
            mixer.music.load(fp)
            mixer.music.play()

            logger.debug("Аудио-приветствие по имени воспроизводится")
            while mixer.music.get_busy():
                time.Clock().tick(10)

            operations_logger.info("USER_LOGIN: Пользователь %s начал работу", self.name)
        except Exception as e:
            error_logger.error("Ошибка при обработке имени пользователя: %s", e, exc_info=True)
            logger.warning("Имя пользователя не обработано")

    def take_inputs(self):
        logger.info("Начало ввода данных от пользователя")

        while True:
            try:
                logger.debug("Запрос первого числа")
                pprint("Enter your first number")
                self.num1 = float(input())
                logger.info("Первое число получено: %.2f", self.num1)
                break
            except ValueError as e:
                error_logger.warning("Некорректный ввод первого числа: %s", e)
                pprint("Please Enter A Valid Number")
                continue

        while True:
            try:
                logger.debug("Запрос второго числа")
                pprint("Enter your second number")
                self.num2 = float(input())
                logger.info("Второе число получено: %.2f", self.num2)
                break
            except ValueError as e:
                error_logger.warning("Некорректный ввод второго числа: %s", e)
                pprint("Please Enter A Valid Number")
                continue

        logger.info("Ввод данных завершен")

    def run_operation(self, operation_name):
        logger.info("Запуск операции: %s", operation_name)

        try:
            if operation_name == "add":
                result = self.add()
            elif operation_name == "sub":
                result = self.sub()
            elif operation_name == "multi":
                result = self.multi()
            elif operation_name == "div":
                result = self.div()
            elif operation_name == "power":
                result = self.power()
            elif operation_name == "root":
                result = self.root()
            elif operation_name == "remainder":
                result = self.remainder()
            elif operation_name == "cube_root":
                result = self.cube_root()
            elif operation_name == "cube_exponent":
                result = self.cube_exponent()
            elif operation_name == "square_root":
                result = self.square_root()
            elif operation_name == "square_exponent":
                result = self.square_exponent()
            else:
                error_logger.error("Неизвестная операция: %s", operation_name)
                raise ValueError(f"Неизвестная операция: {operation_name}")

            logger.info("Операция %s выполнена успешно, результат: %.2f", operation_name, result)
            return result

        except Exception as e:
            error_logger.error("Ошибка при выполнении операции %s: %s", operation_name, e, exc_info=True)
            raise

    class UnitConversion:
        def __init__(self):
            self.logger = logging.getLogger('calculator.unit_conversion')
            self.logger.debug("Инициализация модуля конвертации единиц")
            self.take_inputs()

        def length(self):
            self.logger.info("Конвертация единиц длины")
            pass

        def take_inputs(self):
            self.logger.debug("Ввод данных для конвертации единиц")
            pass

    class Trigonometry:
        def __init__(self):
            self.logger = logging.getLogger('calculator.trigonometry')
            self.logger.debug("Инициализация модуля тригонометрии")

        def pythagorean_theorem(self):
            self.logger.info("Вычисление по теореме Пифагора")
            pass


def demonstrate_calculator():
    logger.info("=" * 50)
    logger.info("ЗАПУСК ДЕМОНСТРАЦИИ КАЛЬКУЛЯТОРА")
    logger.info("=" * 50)

    try:
        calc = Calculator()

        calc.greeting()
        calc.user_name()

        logger.info("Начало выполнения операций")

        operations = [
            ("add", "Сложение"),
            ("sub", "Вычитание"),
            ("multi", "Умножение"),
            ("div", "Деление"),
            ("power", "Возведение в степень"),
            ("square_exponent", "Возведение в квадрат")
        ]

        for op_code, op_name in operations:
            try:
                logger.info("--- Выполнение операции: %s ---", op_name)
                result = calc.run_operation(op_code)
                print(f"{op_name}: {result}")

            except Exception as e:
                logger.warning("Операция %s пропущена из-за ошибки: %s", op_name, str(e))
                print(f"Ошибка в операции {op_name}: {e}")

        logger.info("--- Тестирование обработки ошибок ---")

        calc.num2 = 0
        try:
            result = calc.div()
        except ZeroDivisionError as e:
            logger.error("Ожидаемая ошибка деления на ноль: %s", e)
            print(f"Ожидаемая ошибка: {e}")

        calc.num2 = 5

        logger.info("Демонстрация завершена успешно")

    except Exception as e:
        error_logger.critical("КРИТИЧЕСКАЯ ОШИБКА В ДЕМОНСТРАЦИИ: %s", e, exc_info=True)
        print(f"Критическая ошибка: {e}")
    finally:
        logger.info("=" * 50)
        logger.info("ЗАВЕРШЕНИЕ ДЕМОНСТРАЦИИ КАЛЬКУЛЯТОРА")
        logger.info("=" * 50)


if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("ЗАПУСК ПРИЛОЖЕНИЯ КАЛЬКУЛЯТОР")
    logger.info("Версия: %s", __version__)
    logger.info("Автор: %s", __author__)
    logger.info("=" * 60)

    try:
        demonstrate_calculator()

        logger.info("Приложение завершило работу успешно")
        print("\n" + "=" * 50)
        print("Работа завершена. Проверьте файлы логов:")
        print("- calculator.log - подробные логи")
        print("- calculator_errors.log - ошибки")
        print("- calculator_audit.log - аудит операций")
        print("=" * 50)

    except KeyboardInterrupt:
        logger.warning("Приложение прервано пользователем (Ctrl+C)")
        print("\nРабота прервана пользователем")
    except Exception as e:
        error_logger.critical("Непредвиденная ошибка в основном потоке: %s", e, exc_info=True)
        print(f"\nНепредвиденная ошибка: {e}")
    finally:
        logger.info("=" * 60)
        logger.info("ЗАВЕРШЕНИЕ РАБОТЫ ПРИЛОЖЕНИЯ")
        logger.info("=" * 60)