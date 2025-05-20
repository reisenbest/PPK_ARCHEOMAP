

import config
import sys
import os

from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtSql import QSqlError
from typing import List, Dict, Union
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
        # подключение БД, инициализация
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        # формирует путь к файлу базы данных.
        self.db_path = os.path.join(config.DATABASE_DIR, 'database.db')
        # говорим QT какую БД использовать для подключения
        self.db.setDatabaseName(self.db_path)

        # выкидывает ошибку и закрывает приложение если не удалось открыть БД
        if not self.db.open():
            raise Exception(
                f"Не удалось открыть базу данных: {self.db.lastError().text()}")

        # Включаем поддержку внешних ключей — важно передать self.db - подключение которое используется
        QSqlQuery("PRAGMA foreign_keys = ON", self.db)

    def close(self) -> None:
        """Закрыть соединение с базой данных."""
        self.db.close()

        """
        SELECT 
            m.monument_id,
            m.name,
            m.description,
            m.research_object
            c.latitude,
            c.longitude,
            c.note
        FROM Monuments m
        LEFT JOIN 
            Coordinates c
            ON m.monuments_id c.monuments_id


        """

    def get_monuments(self):
        """Получить список памятников (ID и имя).
        """
        # создание запроса с на получение полей id & name из таблицы  Monuments
        # создание пустого списка для их хранения
        # идем по записям пока они не кончатся и добалвяем в список словарь  1 столбец из полученной строки в id 2 столбец в name
        # возвращает список памятников где каждый памятник - отдельный словарь
        query = QSqlQuery("""
                            SELECT 
                                m.monument_id,
                                m.name,
                                m.description,
                                m.research_object,
                                c.latitude,
                                c.longitude,
                                c.note
                            FROM Monuments m
                            LEFT JOIN Coordinates c ON m.monument_id = c.monument_id
                        """, self.db_manager.db)

        monuments = []
        while query.next():
            record = {}
            columns_count = query.record().count()
            for i in range(columns_count):
                column_name = query.record().fieldName(i)
                column_value = query.value(i)
                record[column_name] = column_value
            monuments.append(record)

        return monuments

    def get_monument_by_id(self, monument_id: int):
        validator = ValidateSQLLevelManager(
            db_manager=self, monument_data=monument_id)
        is_valid, error_msg = validator.validate_read_method()
        if not is_valid:
            # Возвращаем или выбрасываем ошибку, чтобы контроллер мог её обработать
            raise Exception(error_msg)
        """Получить один памятник по ID."""

        # Создаём объект запроса QSqlQuery, связанный с текущим подключением к базе данных
        query = QSqlQuery(self.db)

        # Подготавливаем SQL-запрос с параметром-заполнителем '?'
        # Запрос выбирает все столбцы (*) из таблицы Monuments, где поле monument_id равно переданному параметру
        query.prepare("""
                            SELECT 
                                m.monument_id,
                                m.name,
                                m.description,
                                m.research_object,
                                c.latitude,
                                c.longitude,
                                c.note
                            FROM Monuments m
                            LEFT JOIN Coordinates c ON m.monument_id = c.monument_id
                            WHERE m.monument_id = ?
                        """)

        # Привязываем конкретное значение monument_id к параметру '?' в SQL-запросе
        query.addBindValue(monument_id)

        # Выполняем запрос и проверяем, что он выполнен успешно и что получена хотя бы одна запись
        if query.exec() and query.next():

            # Если запись есть, создаём пустой словарь для хранения данных из результата
            record = {}

            # Получаем количество столбцов в записи (результате запроса)
            columns_count = query.record().count()

            # Перебираем все столбцы в записи по индексам от 0 до количества столбцов - 1
            for i in range(columns_count):

                # Получаем имя текущего столбца по индексу i
                column_name = query.record().fieldName(i)

                # Получаем значение поля из результата запроса по индексу i
                column_value = query.value(i)

                # Записываем пару ключ-значение в словарь: имя столбца — значение этого столбца
                record[column_name] = column_value

            # Возвращаем словарь с данными памятника (все поля из таблицы)
            print(record)
            return record

        # Если запрос не выполнился или запись с таким monument_id не найдена — возвращаем None
        return None

    def create_monument(self, data: dict):
        """Создать новый памятник."""

        """Создать новый памятник с проверкой валидации на уровне БД."""
        # Создаём экземпляр валидатора и передаём self (db_manager) и данные
        validator = ValidateSQLLevelManager(
            db_manager=self, monument_data=data)

        # Проверяем валидацию
        is_valid, error_msg = validator.validate_create_method()
        if not is_valid:
            # Возвращаем или выбрасываем ошибку, чтобы контроллер мог её обработать
            raise Exception(error_msg)

        self.monument_data = data
        query = QSqlQuery(self.db)
        query.prepare("""
            INSERT INTO Monuments (name, description, research_object)
            VALUES (?, ?, ?)
        """)

        query.addBindValue(self.monument_data['name'])
        query.addBindValue(self.monument_data['description'])
        query.addBindValue(self.monument_data['research_object'])
        if not query.exec():
            raise Exception(
                f"Ошибка при добавлении памятника: {query.lastError().text()}")

        return True  # возвращается True если все успешно. Это тру потом используется при CRUD операциях, при обработке ошибок и обновлении окна со списоком памятников после CRUD операций

    def update_monument_by_id(self, monument_id: int, monument: dict):
        """
        Обновить поля памятника по ID.
        Универсальный вариант — список полей задаётся динамически через словарь monument.
        """
        monument_id = {'monument_id': monument_id}
        if not monument:
            return  # Нечего обновлять

        validator = ValidateSQLLevelManager(
            db_manager=self, monument_data=monument)
        # Проверяем валидацию
        is_valid, error_msg = validator.validate_update_method()
        if not is_valid:
            # Возвращаем или выбрасываем ошибку, чтобы контроллер мог её обработать
            raise Exception(error_msg)

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
            raise Exception(
                f"Ошибка при обновлении памятника: {query.lastError().text()}")

        return True  # возвращается True если все успешно. Это тру потом используется при CRUD операциях, при обработке ошибок и обновлении окна со списоком памятников после CRUD операций

    def delete_monument_by_id(self, monument_id: int):
        """Удалить памятник по ID."""
        validator = ValidateSQLLevelManager(
            db_manager=self, monument_data=monument_id)
        is_valid, error_msg = validator.validate_read_method()
        if not is_valid:
            # Возвращаем или выбрасываем ошибку, чтобы контроллер мог её обработать
            raise Exception(error_msg)

        query = QSqlQuery(self.db)
        query.prepare("DELETE FROM Monuments WHERE monument_id = ?")
        query.addBindValue(monument_id)
        if not query.exec():
            raise Exception(
                f"Ошибка при удалении памятника: {query.lastError().text()}")

        return True  # возвращается True если все успешно. Это тру потом используется при CRUD операциях, при обработке ошибок и обновлении окна со списоком памятников после CRUD операций

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
                # Порядковый номер столбца
                "cid": query.value(0),
                "name": query.value(1),                   # Имя столбца
                # Тип данных (например, TEXT, INTEGER)
                "type": query.value(2),
                # True, если поле обязательно для заполнения
                "notnull": bool(query.value(3)),
                # Значение по умолчанию (или None)
                "default_value": query.value(4),
                # True, если это поле является частью первичного ключа
                "primary_key": bool(query.value(5))
            }

            # Добавляем словарь с информацией о колонке в общий список
            table_data.append(column_info)

        # Возвращаем список словарей — по одному на каждую колонку таблицы
        return table_data

# TODO  НАПИСАТЬ В БД КЛАССЕ МЕТОДЫ КРУД И СЕРИАЛИЗАТОРЫ А В КЛАССАХ ИХ ИМПОРТИРОВАТЬ И ВЫЗЫВАТЬ!


class ValidateSQLLevelManager:
    """
    Проверяет валидацию на уровне БД — уникальность имени памятника.
    """

    def __init__(self, db_manager, monument_data: dict, ):
        self.db_manager = db_manager
        self.db = db_manager.db  # доступ к QSqlDatabase
        self.monument_data = monument_data

    def validate_create_method(self) -> (bool, str):
        checks = [
            # self._check_name_not_empty,
            self._check_name_unique_create_method,
            # self._check_description,
            # self._check_research_object,
        ]
        for check in checks:
            ok, msg = check()
            if not ok:
                return False, msg
        return True, ""

    def validate_read_method(self) -> (bool, str):
        checks = [
            self._check_exist_monument_id
        ]
        for check in checks:
            ok, msg = check()
            if not ok:
                return False, msg
        return True, ""

    def validate_update_method(self) -> (bool, str):
        checks = [
            # self._check_name_not_empty,
            self._check_name_unique_update_method,
            # self._check_description,
            # self._check_research_object,
        ]
        for check in checks:
            ok, msg = check()
            if not ok:
                return False, msg
        return True, ""

    def _check_name_not_empty(self):
        pass

    def _check_name_unique_create_method(self):
        name = self.monument_data.get('name', '').strip()
        query = QSqlQuery(self.db)
        query.prepare("SELECT COUNT(*) FROM Monuments WHERE name = ?")
        query.addBindValue(name)
        if not query.exec():
            return False, f"Ошибка при выполнении SQL-запроса: {query.lastError().text()}"
        if query.next() and query.value(0) > 0:
            return False, f"Памятник с именем '{name}' уже существует"
        return True, ""

    def _check_description(self):
        pass

    def _check_research_object(self):
        pass

    def _check_name_unique_update_method(self):
        name = self.monument_data.get('name', '').strip()
        current_id = self.monument_data.get(
            'monument_id')  # Получаем ID текущей записи

        query = QSqlQuery(self.db)
        query.prepare("""
            SELECT COUNT(*) 
            FROM Monuments 
            WHERE name = ? AND monument_id != ?
        """)
        query.addBindValue(name)
        query.addBindValue(current_id)  # Исключаем текущую запись из проверки

        if not query.exec():
            return False, f"Ошибка при выполнении SQL-запроса: {query.lastError().text()}"

        if query.next() and query.value(0) > 0:
            return False, f"Памятник с именем '{name}' уже существует"

        return True, ""

    def _check_exist_monument_id(self) -> bool:
        """
        Проверяет, существует ли памятник с monument_id из self.monument_data в базе.

        Возвращает:
            True, если запись с таким monument_id существует,
            False, если нет или monument_id не задан.
        """
        monument_id = self.monument_data
        query = QSqlQuery(self.db_manager.db)
        query.prepare("SELECT COUNT(*) FROM Monuments WHERE monument_id = ?")
        query.addBindValue(monument_id)
        if query.exec() and query.next():
            count = query.value(0)
            if count > 0:
                return True, ""
            else:
                return False, f"Памятник с ID {monument_id} не найден."
        return False, "Ошибка при проверке существования памятника."


# print('asds')

# x = DataBaseManager()

# details = x.get_info_about_table('Monuments')
# print(details)  # ← без этого ничего не будет видно
