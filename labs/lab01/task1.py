"""Модуль для виконання Завдання 1: Комплексний аналізатор надійності паролів."""

import os
import random
import sys

# Додаємо шлях до кореня проєкту для імпорту shared.student
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
)
from shared.student import GROUP_NAME, STUDENT_NAME, VARIANT_NUMBER  # noqa: E402


def evaluate_password(password: str, criteria: dict, forbidden: set, all_passwords: list) -> str:
    """Проста та зрозуміла оцінка надійності пароля."""
    min_len = criteria["min_length"]

    # 1. Заборонений або занадто короткий
    if password in forbidden or len(password) < min_len:
        return "Заборонений"

    # Перевірка наявності символів за групами
    has_digit = any(c.isdigit() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_special = any(not c.isalnum() for c in password)

    score = sum([has_digit, has_upper, has_lower, has_special])

    # 2. Слабкий (виконує менше 2 критеріїв)
    if score < 2:
        return "Слабкий"

    # 3. Середній (виконує 2-3 критерії або довжина менша за min_length + 4)
    if score < 4 or len(password) < min_len + 4:
        return "Середній"

    # Перевірка на унікальність у списку
    is_unique = all_passwords.count(password) == 1

    # 4. Дуже сильний (всі 4 критерії, довжина достатня і пароль унікальний)
    if score == 4 and len(password) >= min_len + 4 and is_unique:
        return "Дуже сильний"

    # 5. Сильний (всі критерії, але повторюється в списку)
    return "Сильний"


def main() -> None:
    """Головна функція."""
    print(f"Студент: {STUDENT_NAME} | Група: {GROUP_NAME} | Варіант: {VARIANT_NUMBER}")
    print("-" * 60)

    # вхідні дані
    passwords = [
        "APT@Detect10n",
        "simple",
        "Red@Team2023",
        "participant",
        "Blue@T3am",
        "common123",
        "Purple@T34m",
        "regular123",
        "Gr33n@Team",
        "normal123",
    ]
    criteria = {
        "min_length": 7,
        "require_digits": True,
        "require_upper": True,
        "require_special": True,
    }
    forbidden_passwords = {
        "simple",
        "participant",
        "common123",
        "regular123",
        "normal123",
        "test",
    }

    # дублювання 3 результатів
    random_indices = random.sample(range(len(passwords)), 3)
    for idx in random_indices:
        passwords.append(passwords[idx])

    # таблиця результатів
    print(f"{'№':<3} | {'Пароль':<18} | {'Довжина':<8} | {'Результат'}")
    print("-" * 50)

    for i, pwd in enumerate(passwords, start=1):
        result = evaluate_password(pwd, criteria, forbidden_passwords, passwords)
        print(f"{i:<3} | {pwd:<18} | {len(pwd):<8} | {result}")

    print("-" * 50)


if __name__ == "__main__":
    main()