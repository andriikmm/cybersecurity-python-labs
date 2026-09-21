"""Модуль для виконання Завдання 2: Багаторівнева система контролю доступу."""

import os
import sys

# Підключення шляху до кореня для імпорту даних студента
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
)
from shared.student import GROUP_NAME, STUDENT_NAME, VARIANT_NUMBER  # noqa: E402


def main() -> None:
    """Головна точка входу для перевірки доступу."""
    print(f"Студент: {STUDENT_NAME} | Група: {GROUP_NAME} | Варіант: {VARIANT_NUMBER}")
    print("-" * 65)

    # Оголошення вхідних даних для 11 варіанту
    users = {
        "risk_manager": {
            "role": "risk_analyst",
            "clearance": 4,
            "department": "Risk Management",
            "active": True,
        },
        "business_analyst": {
            "role": "business_analyst",
            "clearance": 2,
            "department": "Business",
            "active": True,
        },
        "legal_counsel": {
            "role": "legal",
            "clearance": 3,
            "department": "Legal",
            "active": True,
        },
        "contractor_dev": {
            "role": "contractor",
            "clearance": 2,
            "department": "Contract",
            "active": True,
        },
        "obsolete_system": {
            "role": "legacy_system",
            "clearance": 1,
            "department": "Legacy",
            "active": False,
        },
    }

    resources = [
        ("risk_registers", 4),
        ("business_requirements", 2),
        ("legal_documents", 3),
        ("contract_code", 2),
        ("governance_framework", 4),
        ("meeting_minutes", 1),
        ("regulatory_reports", 3),
        ("executive_dashboards", 4),
        ("project_specs", 2),
        ("public_statements", 1),
    ]

    security_levels = (
        "Public",
        "Internal Use",
        "Restricted",
        "Highly Restricted",
    )
    blocked_users = {"obsolete_system", "contract_expired", "legal_hold"}

    # Виведення списку ресурсів із заміною числових рівнів на текстові назви
    print("Список ресурсів системи:")
    for res_name, level_num in resources:
        level_name = security_levels[level_num - 1]
        print(f" - {res_name:<25} -> {level_name} (рівень {level_num})")

    print("=" * 65)
    print("Результати перевірки доступу:")
    print("-" * 65)

    # Перевірка доступу кожного користувача до кожного ресурсу
    for username, user_info in users.items():
        for res_name, res_level in resources:
            # Перевірка наявності користувача в списку заблокованих
            if username in blocked_users:
                decision = "DENY"
                reason = "User is blocked"
            # Перевірка активності облікового запису
            elif not user_info.get("active", True):
                decision = "DENY"
                reason = "Account inactive"
            else:
                # Порівняння рівня допуску користувача з вимогами ресурсу
                user_clearance = user_info.get("clearance", 0)
                if user_clearance >= res_level:
                    decision = "ALLOW"
                else:
                    decision = "DENY"
                    reason = "Insufficient clearance"

            # Форматування та виведення результату перевірки
            if decision == "ALLOW":
                print(f"user={username:<18} resource={res_name:<22} -> ALLOW")
            else:
                print(f"user={username:<18} resource={res_name:<22} -> DENY ({reason})")

    print("-" * 65)


if __name__ == "__main__":
    main()