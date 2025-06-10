from typing import List, Dict, Union
from PyQt5.QtSql import QSqlError
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from typing import List, Dict

from database.db_validate import ValidateSQLLevelManager
from database.db_queries import DataBaseQueries
import sys
import os
# TODO сделать одну точку входа базы данных при входе в приложение открывается коннект и им все пользуются
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import config


class DataBaseManager:
    '''
    Базовый Класс для работы с БД SQLite через QtSql.
    Поддерживает единое подключение и основные CRUD-операции.
    '''
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataBaseManager, cls).__new__(cls)
            cls._instance._init_db()
        return cls._instance

    def _init_db(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db_path = os.path.join(config.DATABASE_DIR, 'database.db')
        self.db.setDatabaseName(self.db_path)
        self.db_queries = DataBaseQueries()

        if not self.db.open():
            raise Exception(
                f"Не удалось открыть базу данных: {self.db.lastError().text()}")

        QSqlQuery("PRAGMA foreign_keys = ON", self.db)

    def close(self) -> None:
        """Закрыть соединение с базой данных."""
        if self.db.isOpen():
            self.db.close()
            # QSqlDatabase.removeDatabase("qt_sql_default_connection")  # если singleton
    
    def _execute_query(self, query_str: str, values: list = None, error_msg: str = None):
         #prepare + bind + exec (подготовка скл запроса, подстановка параметров, запрос)
        query = QSqlQuery(self.db)
        query.prepare(query_str)
        if values:
            for value in values:
                query.addBindValue(value)
        if not query.exec():
            raise Exception(error_msg or query.lastError().text())
        return query 
    
    def _parse_query_result(self, query_obj, required_field: str = None) -> list[dict]:
        results = []
        record = query_obj.record()
        columns_count = record.count()
        columns_names = [record.fieldName(i) for i in range(columns_count)]

        while query_obj.next():
            if required_field:
                required_value = query_obj.value(required_field)
                if not required_value:
                    continue  # пропускаем строки без обязательного поля

            entry_dict = {}
            for name in columns_names:
                entry_dict[name] = query_obj.value(name)
            results.append(entry_dict)

        return results
               
               
  

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


class DataBaseMonumentsTableManager:
    """docstrDataBaseMonumentTableManager."""
    def __init__(self, db_manager: DataBaseManager, db_queries):
        self.db = db_manager.db
        self.db_queries = db_queries
        self.db_manager_common = db_manager

    def get_monuments(self):
        query = QSqlQuery(self.db_queries.get_monuments(), self.db)
        monuments = {}

        while query.next():
            monument_id = query.value("monument_id")

            if monument_id not in monuments:
                # Инициализируем памятник с координатами сразу
                latitude = query.value("latitude")
                longitude = query.value("longitude")
                note = query.value("note") 

                monuments[monument_id] = {
                    "monument_id": monument_id,
                    "name": query.value("name"),
                    "description": query.value("description"),
                    "research_object": query.value("research_object"),
                    "latitude": latitude,
                    "longitude": longitude,
                    "note": note,
                    "files": [],
                    'excavation_squares': [],

                }

                get_files_query = self.db_manager_common._execute_query(self.db_queries.get_files_by_monument_id_query(),
                                               [monument_id,],
                                               error_msg='error with get files  by monuument id')
                files = self.db_manager_common._parse_query_result(get_files_query, 'file_path')
                if files not in monuments[monument_id]["files"]:
                    monuments[monument_id]["files"].append(files) 

                excavation_squares_query = self.db_manager_common._execute_query(self.db_queries.get_excavation_squares_by_monument_id_query(),
                                               [monument_id,],
                                               error_msg='error with get excavation_squares  by monuument id')
                
                excavation_squares = self.db_manager_common._parse_query_result(excavation_squares_query, 'geometry')
                if excavation_squares not in monuments[monument_id]["excavation_squares"]:
                    monuments[monument_id]["excavation_squares"].append(excavation_squares) 
                print('kekekeke', excavation_squares)


        print(list(monuments.values()))
        return list(monuments.values())

    def get_monument_by_id(self, monument_id: int):
        # --- ВАЛИДАЦИЯ ---
        validator = ValidateSQLLevelManager(
            db_manager=self, monument_data=monument_id)
        is_valid, error_msg = validator.validate_read_method()
        if not is_valid:
            raise Exception(error_msg)

        # --- Получение памятника и координат ---
        #prepare + bind + exec (подготовка скл запроса, подстановка параметров, запрос)
        query = self.db_manager_common._execute_query(self.db_queries.get_monument_by_id_query(),
                                               [monument_id,],
                                               error_msg='error with get monuument by id')

        if query.exec() and query.next():
            record = {}
            columns_count = query.record().count()
            for i in range(columns_count):
                column_name = query.record().fieldName(i)
                column_value = query.value(i)
                record[column_name] = column_value

            # --- Получение файлов ---
            files_query = self.db_manager_common._execute_query(
                self.db_queries.get_files_by_monument_id_query(),
                [monument_id,],
                error_msg=f'ошибка при получении файлов, связанных с памятником {monument_id}'
            )
            excavation_squares_query = self.db_manager_common._execute_query(
                self.db_queries.get_excavation_squares_by_monument_id_query(),
                [monument_id,],
                error_msg=f'ошибка при получении excavation squares, связанных с памятником {monument_id}'
            )
            
            files = self.db_manager_common._parse_query_result(files_query, 'file_path')
            excavation_squares = self.db_manager_common._parse_query_result(excavation_squares_query, 'geometry')

            record["files"] = files
            record["excavation_squares"] = excavation_squares
            print('record', record)
            return record

        return None

    def create_monument(self, data: dict):
        """
        Создаёт памятник и, при наличии, добавляет координаты и связанные файлы.
        """
        if not data:
            raise Exception("Нет данных для создания памятника")

        # --- Разделение данных ---
        monument_fields = {"name", "description", "research_object"}
        coordinates_fields = {"latitude", "longitude", "note"}

        monument_data = {k: v for k, v in data.items() if k in monument_fields}
        coord_data = {k: v for k, v in data.items() if k in coordinates_fields}
        files_data = data.get("files", [])

        # --- Валидация ---
        validator = ValidateSQLLevelManager(
            db_manager=self, monument_data=data)
        is_valid, error_msg = validator.validate_create_method()
        if not is_valid:
            raise Exception(error_msg)

        # --- Вставка памятника ---
        #prepare + bind + exec (подготовка скл запроса, подстановка параметров, запрос)
        query = self.db_manager_common._execute_query(self.db_queries.create_monument(),
                                               [monument_data.get('name'), monument_data.get('description'), monument_data.get('research_object')],
                                               error_msg='ошибка при создании памятника')
        monument_id = query.lastInsertId()

        # --- Вставка координат ---
        if coord_data:
            fields_clause = ", ".join(coord_data.keys()) + ", monument_id"
            placeholders = ", ".join(["?"] * len(coord_data)) + ", ?"
            
            query_str = self.db_queries.create_coordinate(fields_clause, placeholders)
            bind_values = list(coord_data.values()) + [monument_id]  # Собираем все значения для подстановки
            
            self.db_manager_common._execute_query(query_str, bind_values, error_msg=f"Ошибка при добавлении координат")

        # --- Вставка файлов ---
        for file in files_data:
            file_path = file.get("file_path")
            file_type = file.get("file_type", None)
            file_description = file.get("file_description", None)

            if not file_path:
                continue  # обязательное поле

            self.db_manager_common._execute_query(self.db_queries.create_file(), [file_path, file_type, file_description, monument_id])

        return True

    def update_monument_by_id(self, monument_id: int, monument: dict):
        """
        Обновить памятник и его координаты по monument_id.
        """
        if not monument:
            return

        # Разделение на поля Monuments и Coordinates
        monument_fields = {"name", "description", "research_object"}
        coordinates_fields = {"latitude", "longitude", "note"}

        monument_data = {k: v for k, v in monument.items() if k in monument_fields}
        coord_data = {k: v for k, v in monument.items() if k in coordinates_fields}

        # Валидация
        validator = ValidateSQLLevelManager(db_manager=self, monument_data=monument)
        is_valid, error_msg = validator.validate_update_method()
        if not is_valid:
            raise Exception(error_msg)

        # === Обновление Monuments ===
        if monument_data:
            set_parts = [f"{key} = ?" for key in monument_data.keys()]
            set_clause = ", ".join(set_parts)
            values = list(monument_data.values()) + [monument_id]

            self.db_manager_common._execute_query(self.db_queries.update_monument_by_id(set_clause=set_clause),
                                values,
                                error_msg="Ошибка при обновлении Monuments"
                                )

        # === Обновление Coordinates ===
        if coord_data:
            # Проверка существования координат
            check_query = self.db_manager_common._execute_query(
                self.db_queries.get_coordinate_by_monument_id(),
                [monument_id],
                error_msg="Ошибка при проверке координат"
            )
            
            coord_exists = check_query.next()
            coord_id = check_query.value(0) if coord_exists else None

            set_parts = [f"{key} = ?" for key in coord_data.keys()]
            set_clause = ", ".join(set_parts)
            values = list(coord_data.values())

            if coord_exists:
                # Обновление существующих координат
                self.db_manager_common._execute_query(self.db_queries.update_coordinate_by_monument_id(set_clause=set_clause),
                                    values + [monument_id],
                                    error_msg="Ошибка при обновлении Coordinates"
                                    )
            else:
                # Вставка новых координат
                fields_clause = ", ".join(coord_data.keys()) + ", monument_id"
                placeholders = ", ".join(["?"] * len(coord_data)) + ", ?"
                
                self.db_manager_common._execute_query(self.db_queries.create_coordinate_by_monument_id(fields_clause=fields_clause, placeholders=placeholders),
                                    values + [monument_id],
                                    error_msg="Ошибка при добавлении Coordinates"
                                    )

        return True
    def delete_monument_by_id(self, monument_id: int):
        """Удалить памятник по ID."""
        validator = ValidateSQLLevelManager(
            db_manager=self, monument_data=monument_id)
        is_valid, error_msg = validator.validate_read_method()
        if not is_valid:
            # Возвращаем или выбрасываем ошибку, чтобы контроллер мог её обработать
            raise Exception(error_msg)
        
        self.db_manager_common._execute_query(self.db_queries.delete_monument_by_id(), [monument_id], error_msg="Ошибка при удалении памятника sql запрос")

        return True  # возвращается True если все успешно. Это тру потом используется при CRUD операциях, при обработке ошибок и обновлении окна со списоком памятников после CRUD операций


class DataBaseFilesTableManager:
    """docstrDataBaseMonumentTableManager."""
    def __init__(self, db_manager: DataBaseManager, db_queries):
        self.db = db_manager.db
        self.db_queries = db_queries
        self.db_manager_common = db_manager

    def delete_file_by_id(self, file_id: int) -> None:
        # Проверяем есть ли файл
        query = self.db_manager_common._execute_query(
            self.db_queries.get_file_path_by_id(),
            [file_id],
            error_msg=f"Файл с ID {file_id} не найден."
        )
        file_path = query.value("file_path")
        
        # Удаляем из системы сам файл
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                raise Exception(f"Не удалось удалить файл: {file_path} — {e}")
            
        # Удаляем из базы путь
        self.db_manager_common._execute_query(self.db_queries.delete_file_by_id(),[file_id], error_msg=f"Ошибка при удалении файла с ID {file_id} из базы данных")    


    def add_file(self, file_path: str, file_type: str, description: str, monument_id: int) -> None:
        """
        Добавить файл в базу данных
        """
        self.db_manager_common._execute_query(self.db_queries.insert_file(), 
                            [file_path, file_type.strip(), description.strip(), monument_id],
                            error_msg=f"Ошибка добавления файла в БД")

    def get_files_for_monument_by_monument_id(self, monument_id: int):
        """
        Получить список файлов, связанных с памятником по его ID
        """
        query = self.db_manager_common._execute_query(self.db_queries.get_files_for_monument_by_monument_id(), [monument_id], error_msg=f"Ошибка при получении файлов для памятника {monument_id}")
        files = self.db_manager_common._parse_query_result(query, 'file_path')
        return files

    
    def update_file_paths(self, file_id: int, new_path: str) -> None:
        """
        Обновить путь к файлу в базе данных
        """
        self.db_manager_common._execute_query(self.db_queries.update_file_paths_query(), [new_path, file_id], error_msg=f"Не удалось обновить путь файла ID {file_id}")

class DataBaseCoordinateTableManager:
    
    def __init__(self, db_manager: DataBaseManager, db_queries):
        self.db = db_manager.db
        self.db_queries = db_queries

    """docstrDataBaseMonumentTableManager."""

class UnionDataBaseManagerController:
    def __init__(self):
        self.db_common = DataBaseManager()
        self.db_queries = DataBaseQueries()

        self.files_table = DataBaseFilesTableManager(self.db_common, self.db_queries)
        self.coordinates_table = DataBaseCoordinateTableManager(self.db_common, self.db_queries)
        self.monuments_table = DataBaseMonumentsTableManager(self.db_common, self.db_queries)
    


# TODO  НАПИСАТЬ В БД КЛАССЕ МЕТОДЫ КРУД И СЕРИАЛИЗАТОРЫ А В КЛАССАХ ИХ ИМПОРТИРОВАТЬ И ВЫЗЫВАТЬ!
