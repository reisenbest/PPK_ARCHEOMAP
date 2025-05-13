import os
import sys

# Добавляем путь к папке `app`, где лежит config.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.db_main_connection import DBHelper
import config


def main():
    db_path = os.path.join(config.DATABASE_DIR, 'database.db')
    print(f"Используем базу данных по пути: {db_path}")

    db_helper = DBHelper(db_path)

    print("📌 Список памятников:")
    try:
        monuments = db_helper.get_monuments()
        for monument in monuments:
            print(monument)
    except Exception as e:
        print("Ошибка при получении списка памятников:", e)

    print("\n📌 Подробности по первому памятнику:")
    if monuments:
        try:
            first_id = monuments[0][0]
            details = db_helper.get_monument_details(first_id)
            print(details)
        except Exception as e:
            print("Ошибка при получении деталей памятника:", e)
    else:
        print("Нет памятников в базе данных.")


if __name__ == "__main__":
    main()
