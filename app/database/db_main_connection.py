import config
import sys
import os

from PyQt5.QtSql import QSqlDatabase
import sqlite3


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


class DBHelper:
    def __init__(self, db_path):
        self.db_path = os.path.join(config.DATABASE_DIR, 'database.db')

    def connect(self):
        """Подключение к базе данных."""
        return sqlite3.connect(self.db_path)

    def get_monuments(self):
        """Получаем список памятников из базы данных."""
        connection = self.connect()
        cursor = connection.cursor()
        # Измените на свой запрос
        cursor.execute("SELECT monument_id, name FROM Monuments")
        monuments = cursor.fetchall()
        connection.close()
        return monuments

    def get_monument_details(self, monument_id):
        """Получаем подробную информацию о памятнике по ID."""
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM Monuments WHERE monument_id=?", (monument_id,))
        details = cursor.fetchone()
        connection.close()
        return details

# TODO  НАПИСАТЬ В БД КЛАССЕ МЕТОДЫ КРУД И СЕРИАЛИЗАТОРЫ А В КЛАССАХ ИХ ИМПОРТИРОВАТЬ И ВЫЗЫВАТЬ!


print('asds')
db_path = os.path.join(config.DATABASE_DIR, 'database.db')
x = DBHelper(db_path)
details = x.get_monument_details(1)
print(details)  # ← без этого ничего не будет видно
