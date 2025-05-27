from typing import List, Dict, Union
from PyQt5.QtSql import QSqlQuery


#вся валидация на урвоне скл хранится здесь
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
