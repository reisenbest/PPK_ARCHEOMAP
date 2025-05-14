
import config
import sys
import os

from PyQt5.QtSql import QSqlDatabase
import sqlite3

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
    Класс для работы с БД с единственным соединением на протяжении жизни приложения.
    '''

    def __init__(self):
        # Путь к базе данных
        self.db_path = os.path.join(config.DATABASE_DIR, 'database.db')
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = self.dict_factory
        self.cursor = self.connection.cursor()

    def dict_factory(self, cursor, row):
        """Формирует результат запроса в виде словаря."""
        return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

    def close(self):
        """Закрываем соединение с базой данных."""
        if self.connection:
            self.connection.close()

    def get_monuments(self):
        """Получаем список памятников из базы данных."""
        self.cursor.execute("SELECT monument_id, name FROM Monuments")
        return self.cursor.fetchall()
        # [{'monument_id': 1, 'name': 'Название'}, ...]

    def get_monument_by_id(self, monument_id: int):
        """Получаем подробную информацию о памятнике по ID."""
        self.cursor.execute(
            "SELECT * FROM Monuments WHERE monument_id=?", (monument_id,))
        result = self.cursor.fetchone()  # Уже будет dict, а не кортеж
        return result  # {'monument_id': ..., 'name': ..., ...}

    def create_monument(self):
        """Ручка на создание одного объекта."""
        pass

    def update_monument_by_id(self, monument_id: int):
        """Ручка на изменение одного объекта по id."""
        pass

    def delete_monument_by_id(self, monument_id: int):
        """Ручка на удаление объекта по id."""
        self.cursor.execute(
            'DELETE FROM Monuments WHERE monument_id = ?', (monument_id,))
        self.connection.commit()


# TODO  НАПИСАТЬ В БД КЛАССЕ МЕТОДЫ КРУД И СЕРИАЛИЗАТОРЫ А В КЛАССАХ ИХ ИМПОРТИРОВАТЬ И ВЫЗЫВАТЬ!

print('asds')

x = DataBaseManager()

details = x.get_monuments()
print(details)  # ← без этого ничего не будет видно
