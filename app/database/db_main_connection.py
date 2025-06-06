import sys
import os
# TODO сделать одну точку входа базы данных при входе в приложение открывается коннект и им все пользуются
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.db_queries import DataBaseQueries
from database.db_validate import ValidateSQLLevelManager
import config
from typing import List, Dict


from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtSql import QSqlError
from typing import List, Dict, Union




class DataBaseManager:
    '''
    Класс для работы с БД SQLite через QtSql.
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
                    "files": []
                }

            # Добавляем файл, если он есть
            file_path = query.value("file_path")
            if file_path:
                file_entry = {
                    "file_path": file_path,
                    "file_type": query.value("file_type"),
                    "file_description": query.value("file_description")
                }
                if file_entry not in monuments[monument_id]["files"]:
                    monuments[monument_id]["files"].append(file_entry)

        return list(monuments.values())

    # def get_monuments(self):
    #     """Получить список памятников (ID и имя).
    #     """
    #     # создание запроса с на получение полей id & name из таблицы  Monuments
    #     # создание пустого списка для их хранения
    #     # идем по записям пока они не кончатся и добалвяем в список словарь  1 столбец из полученной строки в id 2 столбец в name
    #     # возвращает список памятников где каждый памятник - отдельный словарь
    #     query = QSqlQuery(self.db_queries.get_monuments(), self.db)

    #     monuments = []
    #     while query.next():
    #         record = {}
    #         columns_count = query.record().count()
    #         for i in range(columns_count):
    #             column_name = query.record().fieldName(i)
    #             column_value = query.value(i)
    #             record[column_name] = column_value
    #         monuments.append(record)

    #     return monuments

    def get_monument_by_id(self, monument_id: int):
        # --- ВАЛИДАЦИЯ ---
        validator = ValidateSQLLevelManager(db_manager=self, monument_data=monument_id)
        is_valid, error_msg = validator.validate_read_method()
        if not is_valid:
            raise Exception(error_msg)

        # --- Получение памятника и координат ---
        query = QSqlQuery(self.db)
        query.prepare(self.db_queries.get_monument_by_id())
        query.addBindValue(monument_id)

        if query.exec() and query.next():
            record = {}
            columns_count = query.record().count()
            for i in range(columns_count):
                column_name = query.record().fieldName(i)
                column_value = query.value(i)
                record[column_name] = column_value

            # --- Получение файлов ---
            files_query = QSqlQuery(self.db)
            files_query.prepare(self.db_queries.get_files_by_monument_id())
            files_query.addBindValue(monument_id)

            files = []
            if files_query.exec():
                while files_query.next():
                    files.append({
                        "file_id": files_query.value("file_id"),
                        "file_path": files_query.value("file_path"),
                        "file_type": files_query.value("file_type"),
                        "file_description": files_query.value("file_description"),
                        "monument_id": files_query.value("monument_id")
                    })

            record["files"] = files
            print('recorc', record)
            return record

        return None
    
    def get_files_for_monument_by_monument_id(self, monument_id: int):
        query = QSqlQuery(self.db)
        query.prepare(self.db_queries.get_files_for_monument_by_monument_id())
        query.addBindValue(monument_id)

        if not query.exec():
            raise Exception(f"Ошибка при выполнении запроса: {query.lastError().text()}")

        files = []
        while query.next():
            files.append({
                "file_id": query.value("file_id"),
                "file_path": query.value("file_path"),
                "file_type": query.value("file_type"),
                "file_description": query.value("file_description")
            })
        return files


    def create_monument(self, data: dict):
        """
        Создаёт памятник и, при наличии, добавляет координаты и связанные файлы.

        Ожидаемый формат данных:
        {
            "name": str,
            "description": str,
            "research_object": str,
            "latitude": float,
            "longitude": float,
            "note": str,
            "files": [
                {
                    "file_path": str,
                    "file_type": str,
                    "file_description": str
                },
                ...
            ]
        }
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
        validator = ValidateSQLLevelManager(db_manager=self, monument_data=data)
        is_valid, error_msg = validator.validate_create_method()
        if not is_valid:
            raise Exception(error_msg)

        # --- Вставка памятника ---
        query = QSqlQuery(self.db)
        query.prepare(self.db_queries.create_monument())
        query.addBindValue(monument_data.get('name'))
        query.addBindValue(monument_data.get('description'))
        query.addBindValue(monument_data.get('research_object'))

        if not query.exec():
            raise Exception(f"Ошибка при добавлении памятника: {query.lastError().text()}")

        monument_id = query.lastInsertId()

        # --- Вставка координат ---
        if coord_data:
            fields_clause = ", ".join(coord_data.keys()) + ", monument_id"
            placeholders = ", ".join(["?"] * len(coord_data)) + ", ?"

            coord_query = QSqlQuery(self.db)
            coord_query.prepare(self.db_queries.create_coordinate(fields_clause, placeholders))

            for value in coord_data.values():
                coord_query.addBindValue(value)
            coord_query.addBindValue(monument_id)

            if not coord_query.exec():
                raise Exception(f"Ошибка при добавлении координат: {coord_query.lastError().text()}")

        # --- Вставка файлов ---
        for file in files_data:
            file_path = file.get("file_path")
            file_type = file.get("file_type", None)
            file_description = file.get("file_description", None)

            if not file_path:
                continue  # обязательное поле

            file_query = QSqlQuery(self.db)
            file_query.prepare(self.db_queries.create_file())
            file_query.addBindValue(file_path)
            file_query.addBindValue(file_type)
            file_query.addBindValue(file_description)
            file_query.addBindValue(monument_id)

            if not file_query.exec():
                raise Exception(f"Ошибка при добавлении файла: {file_query.lastError().text()}")

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
        

        # формирование словаря только с полями относящимися к монументс
        monument_data = {k: v for k,
                         v in monument.items() if k in monument_fields}
        # формирование словаря только с полями относящимися к координатами
        coord_data = {k: v for k, v in monument.items()
                      if k in coordinates_fields}

        # Валидация (если нужно, можно проверить и по частям)
        validator = ValidateSQLLevelManager(
            db_manager=self, monument_data=monument)
        is_valid, error_msg = validator.validate_update_method()
        if not is_valid:
            raise Exception(error_msg)

        # === Обновление Monuments ===
        if monument_data:
            # Создаёт список строк для SQL-запроса обновления, set_parts = ["name = ?", "description = ?"]
            set_parts = [f"{key} = ?" for key in monument_data.keys()]
            # Объединяет элементы set_parts через запятую в одну строку. set_clause = "name = ?, description = ?"
            set_clause = ", ".join(set_parts)
            values = list(monument_data.values())

            query = QSqlQuery(self.db)
            query.prepare(self.db_queries.update_monument_by_id(
                set_clause=set_clause))
            for value in values:
                query.addBindValue(value)
            query.addBindValue(monument_id)

            if not query.exec():
                raise Exception(
                    f"Ошибка при обновлении Monuments: {query.lastError().text()}")

        # === Обновление Coordinates ===
        if coord_data:
            # Проверим, есть ли вообще координаты у этого monument_id
            check_query = QSqlQuery(self.db)
            check_query.prepare(
                self.db_queries.get_coordinate_by_monument_id())
            check_query.addBindValue(monument_id)

            if not check_query.exec():
                raise Exception(
                    f"Ошибка при проверке координат: {check_query.lastError().text()}")

            coord_exists = check_query.next()
            coord_id = check_query.value(0) if coord_exists else None

            set_parts = [f"{key} = ?" for key in coord_data.keys()]
            set_clause = ", ".join(set_parts)
            values = list(coord_data.values())

            if coord_exists:
                # Обновление координат
                query = QSqlQuery(self.db)
                query.prepare(self.db_queries.update_coordinate_by_monument_id(
                    set_clause=set_clause))
                for value in values:
                    query.addBindValue(value)
                query.addBindValue(monument_id)

                if not query.exec():
                    raise Exception(
                        f"Ошибка при обновлении Coordinates: {query.lastError().text()}")

            else:
                # Вставка новой записи в Coordinates
                # Формирует перечень названий колонок, в которые будут вставляться данные. fields_clause = "latitude, longitude, monument_id"
                fields_clause = ", ".join(coord_data.keys()) + ", monument_id"
                # Формирует строку с плейсхолдерами (?) под значения, передаваемые в SQL-запрос. placeholders = "?, ?, ?" сколько в коорд дата элементов столько и вопросиков
                placeholders = ", ".join(["?"] * len(coord_data)) + ", ?"
                query = QSqlQuery(self.db)
                query.prepare(self.db_queries.create_coordinate_by_monument_id(
                    fields_clause=fields_clause, placeholders=placeholders))
                for value in values:
                    query.addBindValue(value)
                query.addBindValue(monument_id)

                if not query.exec():
                    raise Exception(
                        f"Ошибка при добавлении Coordinates: {query.lastError().text()}")

        return True

    def delete_monument_by_id(self, monument_id: int):
        """Удалить памятник по ID."""
        validator = ValidateSQLLevelManager(
            db_manager=self, monument_data=monument_id)
        is_valid, error_msg = validator.validate_read_method()
        if not is_valid:
            # Возвращаем или выбрасываем ошибку, чтобы контроллер мог её обработать
            raise Exception(error_msg)

        query = QSqlQuery(self.db)
        query.prepare(self.db_queries.delete_monument_by_id())
        query.addBindValue(monument_id)
        if not query.exec():
            raise Exception(
                f"Ошибка при удалении памятника: {query.lastError().text()}")

        return True  # возвращается True если все успешно. Это тру потом используется при CRUD операциях, при обработке ошибок и обновлении окна со списоком памятников после CRUD операций

    def delete_file_by_id(self, file_id: int) -> None:
        query = QSqlQuery(self.db)
        query.prepare(self.db_queries.get_file_path_by_id())  # 'SELECT file_path FROM Files WHERE file_id = ?'
        query.addBindValue(file_id)

        if not query.exec() or not query.next():
            raise Exception(f"Файл с ID {file_id} не найден.")

        file_path = query.value("file_path")

        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                raise Exception(f"Не удалось удалить файл: {file_path} — {e}")

        del_query = QSqlQuery(self.db)
        del_query.prepare(self.db_queries.delete_file_by_id())  # 'DELETE FROM Files WHERE file_id = ?'
        del_query.addBindValue(file_id)
        if not del_query.exec():
            raise Exception(f"Ошибка при удалении файла с ID {file_id}: {del_query.lastError().text()}")
    def add_file(self, file_path: str, file_type: str, description: str, monument_id: int) -> None:
        query = QSqlQuery(self.db)
        query.prepare(self.db_queries.insert_file())
        query.addBindValue(file_path)
        query.addBindValue(file_type.strip())
        query.addBindValue(description.strip())
        query.addBindValue(monument_id)

        if not query.exec():
            raise Exception(f"Ошибка добавления файла в БД: {query.lastError().text()}")
            
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


x = DataBaseManager()

print(x.get_monuments())

# TODO  НАПИСАТЬ В БД КЛАССЕ МЕТОДЫ КРУД И СЕРИАЛИЗАТОРЫ А В КЛАССАХ ИХ ИМПОРТИРОВАТЬ И ВЫЗЫВАТЬ!


# print('asds')

# x = DataBaseManager()

# details = x.get_info_about_table('Monuments')
# print(details)  # ← без этого ничего не будет видно
