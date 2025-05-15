
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


class DataBaseManager:
    '''
    Класс для работы с БД SQLite через QtSql.
    Поддерживает единое подключение и основные CRUD-операции.
    '''

    def __init__(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db_path = os.path.join(config.DATABASE_DIR, 'database.db')
        self.db.setDatabaseName(self.db_path)
        self.db.open()
        if self.db.isOpenError():
            raise Exception(f"Не удалось открыть базу данных: {self.db.lastError().text()}")

        QSqlQuery("PRAGMA foreign_keys = ON")  # включаем поддержку внешних ключей

    def close(self):
        """Закрыть соединение с базой данных."""
        self.db.close()

    def get_monuments(self):
        """Получить список памятников (ID и имя)."""
        query = QSqlQuery("SELECT monument_id, name FROM Monuments")
        monuments = []
        while query.next():
            monuments.append({
                "monument_id": query.value(0),
                "name": query.value(1)
            })
        return monuments

    def get_monument_by_id(self, monument_id: int):
        """Получить один памятник по ID."""
        query = QSqlQuery()
        query.prepare("SELECT * FROM Monuments WHERE monument_id = ?")
        query.addBindValue(monument_id)
        if query.exec() and query.next():
            record = {}
            for i in range(query.record().count()):
                record[query.record().fieldName(i)] = query.value(i)
            return record
        return None

    def create_monument(self, name: str, type_id: int):
        """Создать новый памятник."""
        query = QSqlQuery()
        query.prepare("""
            INSERT INTO Monuments (name, type_id)
            VALUES (?, ?)
        """)
        query.addBindValue(name)
        query.addBindValue(type_id)
        if not query.exec():
            raise Exception(f"Ошибка при добавлении памятника: {query.lastError().text()}")

    def update_monument_by_id(self, monument_id: int, fields: dict):
        """
        Обновить поля памятника по ID.
        Пример: fields = {"name": "Новое имя", "type_id": 2}
        """
        if not fields:
            return  # ничего не обновлять

        # Формируем SQL-запрос динамически
        set_clause = ", ".join(f"{key} = ?" for key in fields.keys())
        values = list(fields.values())

        query = QSqlQuery()
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
        query = QSqlQuery()
        query.prepare("DELETE FROM Monuments WHERE monument_id = ?")
        query.addBindValue(monument_id)
        if not query.exec():
            raise Exception(f"Ошибка при удалении памятника: {query.lastError().text()}")

# TODO  НАПИСАТЬ В БД КЛАССЕ МЕТОДЫ КРУД И СЕРИАЛИЗАТОРЫ А В КЛАССАХ ИХ ИМПОРТИРОВАТЬ И ВЫЗЫВАТЬ!

print('asds')

x = DataBaseManager()

details = x.get_monuments()
print(details)  # ← без этого ничего не будет видно
