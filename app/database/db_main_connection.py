
import config
import sys
import os

from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtSql import QSqlError

# TODO сделать одну точку входа базы данных при входе в приложение открывается коннект и им все пользуются
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
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
            INSERT INTO Monuments (name, type_id)
            VALUES (?, ?)
        """)
        query.addBindValue(name)
        query.addBindValue(type_id)
        if not query.exec():
            raise Exception(f"Ошибка при добавлении памятника: {query.lastError().text()}")

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

    def delete_monument_by_id(self, monument_id: int):
        """Удалить памятник по ID."""
        query = QSqlQuery(self.db)
        query.prepare("DELETE FROM Monuments WHERE monument_id = ?")
        query.addBindValue(monument_id)
        if not query.exec():
            raise Exception(f"Ошибка при удалении памятника: {query.lastError().text()}")
        
    def get_info_about_table(self, table_name: str):
        query = QSqlQuery(self.db)
        query.prepare(f"SELECT * FROM {table_name}, LIMIT 1")
        query.addBindValue(table_name)
        if not query.exec():
            raise Exception(f"Ошибка при запросе: {query.lastError().text()}")

        record = query.record()
        data = {}
        #добавить 3 ключа - количество колонок, их названия и тип? или обхеденить? из этого потом в create monument данные брать после его вызова
# TODO  НАПИСАТЬ В БД КЛАССЕ МЕТОДЫ КРУД И СЕРИАЛИЗАТОРЫ А В КЛАССАХ ИХ ИМПОРТИРОВАТЬ И ВЫЗЫВАТЬ!

print('asds')

x = DataBaseManager()

details = x.get_monuments()
print(details)  # ← без этого ничего не будет видно
