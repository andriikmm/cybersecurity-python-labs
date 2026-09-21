"""Головний файл для демонстрації виконання Лабораторної роботи №1."""

import os
import sys

# Додавання шляху до кореня проєкту для коректних імпортів
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
)

# Імпорт головних функцій з кожного файлу завдань
from labs.lab01.task1 import main as run_task1
from labs.lab01.task2 import main as run_task2
from labs.lab01.task3 import main as run_task3


def main() -> None:
    """Послідовний запуск усіх завдань лабораторної роботи №1."""
    print("=== ПОЧАТОК ВИКОНАННЯ ЛАБОРАТОРНОЇ РОБОТИ №1 ===\n")

    print("[ 1 ] ВИКОНАННЯ ЗАВДАННЯ 1: Аналізатор надійності паролів")
    print("=" * 65)
    run_task1()
    print("\n" + "=" * 65 + "\n")

    print("[ 2 ] ВИКОНАННЯ ЗАВДАННЯ 2: Система контролю доступу")
    print("=" * 65)
    run_task2()
    print("\n" + "=" * 65 + "\n")

    print("[ 3 ] ВИКОНАННЯ ЗАВДАННЯ 3: Хешування, CSV-база та логування")
    print("=" * 65)
    run_task3()
    print("\n" + "=" * 65)
    print("=== КІНЕЦЬ ВИКОНАННЯ ЛАБОРАТОРНОЇ РОБОТИ №1 ===")


if __name__ == "__main__":
    main()