"""Модуль для виконання Завдання 3: Безпечне хешування, CSV-база та JSON-логування."""

import csv
import datetime
import hashlib
import json
import os
import sys

# Підключення шляху до кореня для імпорту даних студента
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
)
from shared.student import GROUP_NAME, STUDENT_NAME, VARIANT_NUMBER  # noqa: E402


# Створення власного винятку для валідації довжини пароля
class ValidationError(Exception):
    """Виняток, що викликається, якщо пароль не відповідає критеріям довжини."""

    pass


def log_event(func):
    """Декоратор для запису подій автентифікації у файл log.json."""
    def wrapper(username, password, *args, **kwargs):
        # Виклик оригінальної функції логіну
        result = func(username, password, *args, **kwargs)

        event_data = {
            "event": "login",
            "user": username,
            "result": "success" if result else "failure",
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "args": list(args),
            "kwargs": kwargs,
        }

        log_dir = os.path.join(os.path.dirname(__file__), "data")
        os.makedirs(log_dir, exist_ok=True)
        log_file_path = os.path.join(log_dir, "log.json")

        # Читання існуючих логів або створення нового списку
        logs = []
        if os.path.exists(log_file_path):
            try:
                with open(log_file_path, "r", encoding="utf-8") as f:
                    logs = json.load(f)
            except (json.JSONDecodeError, IOError):
                logs = []

        logs.append(event_data)

        # Запис оновленого списку логів у JSON-файл
        with open(log_file_path, "w", encoding="utf-8") as f:
            json.dump(logs, f, ensure_ascii=False, indent=4)

        return result

    return wrapper


def generate_hash(password: str, salt: str = "00000") -> str:
    """Генерація хешу пароля з використанням алгоритму blake2b та солі для 11 варіанту."""
    if not password or not salt:
        raise ValueError("Пароль або сіль не можуть бути порожніми.")

    # Мінімальна довжина пароля для 11 варіанту становить 12 символів
    min_length = 12
    if len(password) < min_length:
        raise ValidationError(f"Пароль занадто короткий. Мінімальна довжина: {min_length}")

    # Конкатенація пароля та солі
    salted_password = password + salt

    # Використання алгоритму blake2b згідно з 11 варіантом
    hasher = hashlib.new("blake2b")
    hasher.update(salted_password.encode("utf-8"))
    return hasher.hexdigest()


def create_user(username: str, password: str) -> tuple:
    """Створення користувача у форматі кортежу (логін, хеш_пароля)."""
    # Формування персональної солі з номера варіанту (11 варіант -> "00011")
    personal_salt = f"{VARIANT_NUMBER:05d}"
    password_hash = generate_hash(password, personal_salt)
    return (username, password_hash)


def create_users(users_list: tuple) -> None:
    """Створення бази даних та збереження користувачів у CSV-файл."""
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(data_dir, exist_ok=True)
    file_path = os.path.join(data_dir, "users.csv")

    # Запис списку користувачів у CSV-файл
    with open(file_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["username", "password_hash"])
        for username, raw_password in users_list:
            try:
                user_record = create_user(username, raw_password)
                writer.writerow(user_record)
            except (ValueError, ValidationError) as e:
                print(f"Попередження для користувача {username}: {e}")


@log_event
def login(username: str, password: str) -> bool:
    """Автентифікація користувача з перевіркою хешу у CSV-базі."""
    if not username or not password:
        raise ValueError("Логін або пароль не можуть бути порожніми.")

    file_path = os.path.join(os.path.dirname(__file__), "data", "users.csv")

    # Зчитування бази даних та перевірка облікових даних
    with open(file_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        personal_salt = f"{VARIANT_NUMBER:05d}"
        input_hash = generate_hash(password, personal_salt)

        for row in reader:
            if row["username"] == username and row["password_hash"] == input_hash:
                return True

    return False


def main() -> None:
    """Головна функція для запуску перевірки Task 3."""
    print(f"Студент: {STUDENT_NAME} | Група: {GROUP_NAME} | Варіант: {VARIANT_NUMBER}")
    print("-" * 65)

    users_to_register = (
        ("admin_sec11", "SecurePass123!"),
        ("analyst_net", "StrongCrypto@99"),
        ("dev_ops_2023", "P0w3rful#Code"),
        ("auditor_kpi", "AuditCheck$2026"),
        ("guest_user1", "SimplePass1234"),
        ("manager_itx", "ManagerSecret!7"),
        ("support_tech", "HelpDeskCode#55"),
        ("tester_qa_01", "QualityAssure@1"),
        ("lead_architect", "Architecture$88"),
        ("system_root_9", "RootAccess#2026"),
    )

    try:
        create_users(users_to_register)
        print("Базу даних 'users.csv' успішно створено та заповнено.")

        file_path = os.path.join(os.path.dirname(__file__), "data", "users.csv")
        print("\nВміст файлу users.csv:")
        print(f"{'Логін':<20} | {'Хеш пароля'}")
        print("-" * 65)

        with open(file_path, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)  # Пропуск заголовка
            for row in reader:
                print(f"{row[0]:<20} | {row[1]}")

        print("=" * 65)
        print("Тестування автентифікації:")

        success_login = login("admin_sec11", "SecurePass123!")
        print(f"Вхід ('admin_sec11', правильний пароль) -> {success_login}")

        fail_login = login("admin_sec11", "WrongPassword!")
        print(f"Вхід ('admin_sec11', неправильний пароль) -> {fail_login}")

        try:
            login("", "")
        except ValueError as e:
            print(f"Попередження: Очікуваний помилковий виняток: {e}")

    except (FileNotFoundError, PermissionError, IOError) as file_err:
        print(f"Помилка при роботі з файлом: {file_err}")
    except ValidationError as val_err:
        print(f"Помилка валідації: {val_err}")
    except ValueError as val_err:
        print(f"Значеннєва помилка: {val_err}")

    print("-" * 65)


if __name__ == "__main__":
    main()