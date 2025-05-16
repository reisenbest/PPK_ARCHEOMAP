

import sys
import os

from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtSql import QSqlError

# TODO сделать одну точку входа базы данных при входе в приложение открывается коннект и им все пользуются
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config
# class DataBaseConnection(QSqlDatabase):
#   """docstring for ClassName."""
#   def __init__(self, parent=None):
#     super().__init__(parent)
#     self.db_coonnection()

#   def db_coonnection(self):


#     connection_status = db.open()
#     if connection_status:
#       print('succesful connection to database', file=sys.stderr)
#     else:
#       print('connection error', file=sys.stderr)


import os
import config
from PyQt5.QtSql import QSqlDatabase, QSqlQuery


class DataBaseManager:
    '''
    Класс для работы с БД SQLite через QtSql.
    Поддерживает единое подключение и основные CRUD-операции.
    '''

    def __init__(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db_path = os.path.join(config.DATABASE_DIR, 'database.db')
        self.db.setDatabaseName(self.db_path)

        if not self.db.open():
            raise Exception(f"Не удалось открыть базу данных: {self.db.lastError().text()}")

        # Включаем поддержку внешних ключей — важно передать self.db
        QSqlQuery("PRAGMA foreign_keys = ON", self.db)

    def close(self):
        """Закрыть соединение с базой данных."""
        self.db.close()

    def get_monuments(self):
        """Получить список памятников (ID и имя)."""
        query = QSqlQuery("SELECT monument_id, name FROM Monuments", self.db)
        monuments = []
        while query.next():
            monuments.append({
                "monument_id": query.value(0),
                "name": query.value(1)
            })
        return monuments

    def get_monument_by_id(self, monument_id: int):
        """Получить один памятник по ID."""
        query = QSqlQuery(self.db)
        query.prepare("SELECT * FROM Monuments WHERE monument_id = ?")
        query.addBindValue(monument_id)
        if query.exec() and query.next():
            record = {}
            for i in range(query.record().count()):
                record[query.record().fieldName(i)] = query.value(i)
            return record
        return None
    
    def create_monument(self, data: dict):
        """Создать новый памятник."""
        query = QSqlQuery(self.db)
        query.prepare("""
            INSERT INTO Monuments (name, description, research_object)
            VALUES (?, ?, ?)
        """)

        query.addBindValue(data['name'])
        query.addBindValue(data['description'])
        query.addBindValue(data['research_object'])
        if not query.exec():
            raise Exception(f"Ошибка при добавлении памятника: {query.lastError().text()}")

        return True #возвращается True если все успешно. Это тру потом используется при CRUD операциях, при обработке ошибок и обновлении окна со списоком памятников после CRUD операций
    def update_monument_by_id(self, monument_id: int, monument: dict):
        """
        Обновить поля памятника по ID.
        Универсальный вариант — список полей задаётся динамически через словарь monument.
        """
        if not monument:
            return  # Нечего обновлять

        set_parts = [f"{key} = ?" for key in monument.keys()]
        set_clause = ", ".join(set_parts)
        values = list(monument.values())

        query = QSqlQuery(self.db)
        query.prepare(f"""
            UPDATE Monuments
            SET {set_clause}
            WHERE monument_id = ?
        """)

        for value in values:
            query.addBindValue(value)
        query.addBindValue(monument_id)

        if not query.exec():
            raise Exception(f"Ошибка при обновлении памятника: {query.lastError().text()}")

        return True #возвращается True если все успешно. Это тру потом используется при CRUD операциях, при обработке ошибок и обновлении окна со списоком памятников после CRUD операций
    def delete_monument_by_id(self, monument_id: int):
        """Удалить памятник по ID."""
        query = QSqlQuery(self.db)
        query.prepare("DELETE FROM Monuments WHERE monument_id = ?")
        query.addBindValue(monument_id)
        if not query.exec():
            raise Exception(f"Ошибка при удалении памятника: {query.lastError().text()}")
        
        return True #возвращается True если все успешно. Это тру потом используется при CRUD операциях, при обработке ошибок и обновлении окна со списоком памятников после CRUD операций
    def get_info_about_table(self, table_name: str):
        # Создаём объект запроса, используя подключение к базе
        query = QSqlQuery(self.db)

        # Подготавливаем SQL-запрос на получение информации о структуре таблицы
        # PRAGMA table_info(<table_name>) — это специальная команда SQLite,
        # которая возвращает информацию о колонках указанной таблицы.
        # Она не поддерживает параметризованные значения, поэтому имя таблицы вставляется напрямую.
        query.prepare(f"PRAGMA table_info({table_name})")

        # Выполняем запрос
        if not query.exec():
            # Если произошла ошибка — выбрасываем исключение с сообщением
            raise Exception(f"Ошибка при запросе: {query.lastError().text()}")

        # Здесь будет храниться информация обо всех колонках таблицы
        table_data = []

        # Обрабатываем строки результата запроса
        while query.next():
            # Для каждой строки (т.е. каждой колонки в таблице) возвращаются такие поля:
            # 0: cid            — порядковый номер колонки
            # 1: name           — имя колонки
            # 2: type           — тип данных (например, TEXT, INTEGER)
            # 3: notnull        — флаг: 1, если поле не может быть NULL
            # 4: dflt_value     — значение по умолчанию (если задано)
            # 5: pk             — флаг: 1, если это часть первичного ключа

            column_info = {
                "cid": query.value(0),                    # Порядковый номер столбца
                "name": query.value(1),                   # Имя столбца
                "type": query.value(2),                   # Тип данных (например, TEXT, INTEGER)
                "notnull": bool(query.value(3)),          # True, если поле обязательно для заполнения
                "default_value": query.value(4),          # Значение по умолчанию (или None)
                "primary_key": bool(query.value(5))       # True, если это поле является частью первичного ключа
            }

            # Добавляем словарь с информацией о колонке в общий список
            table_data.append(column_info)

        # Возвращаем список словарей — по одному на каждую колонку таблицы
        return table_data

# TODO  НАПИСАТЬ В БД КЛАССЕ МЕТОДЫ КРУД И СЕРИАЛИЗАТОРЫ А В КЛАССАХ ИХ ИМПОРТИРОВАТЬ И ВЫЗЫВАТЬ!

print('asds')

x = DataBaseManager()

details = x.get_info_about_table('Monuments')
print(details)  # ← без этого ничего не будет видно
