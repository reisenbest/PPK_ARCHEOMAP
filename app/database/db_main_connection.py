import sys
import os
import config
from PyQt5.QtSql import QSqlDatabase
import sqlite3


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))) # при запуске приложения через main.py Ошибку при отсутствии этой строчки не выкидывает

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
        cursor.execute("SELECT monument_id, name FROM Monuments")  # Измените на свой запрос
        monuments = cursor.fetchall()
        connection.close()
        return monuments

    def get_monument_details(self, monument_id):
        """Получаем подробную информацию о памятнике по ID."""
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Monuments WHERE id=?", (monument_id,))
        details = cursor.fetchone()
        connection.close()
        return details