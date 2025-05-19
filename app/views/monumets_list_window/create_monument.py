
import os
import sys
import config
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot, QObject
from PyQt5.uic import loadUi
import json
from utils.base_classes import BaseView
from utils.validate_manager import ValidateUILevelManager   
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))




class CreateMonumentView(QDialog, BaseView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_ui('create_monument_window.ui')

    def buttons_placeholders(self, table_info: dict):
        name_placeholder = f'имя столбца: {table_info['name']['name']}, тип: {table_info['name']['type']}'
        description_placeholder = table_info['description']['name']
        research_object_placeholder = table_info['research_object']['name']

        self.nameInsert.setPlaceholderText(name_placeholder)
        self.descriptionInsert.setPlaceholderText(description_placeholder)
        self.resObjInsert.setPlaceholderText(json.dumps(table_info['research_object']))

class CreateMonumentController(QObject):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.view = CreateMonumentView()
        self.db_manager = db_manager
        self.setup_connections()
        self.set_placeholders()
        self.validator = ValidateUILevelManager(db_manager=self.db_manager)

    def show(self):
        self.view.show()

    def setup_connections(self):
        """Настройка подключения кнопок."""
        # Подключаем действия к кнопкам
        self.view.createBtn.clicked.connect(self.create_monument)
        self.view.cancelBtn.clicked.connect(self.cancel_create)  # Обработчик кнопки "Отмена

    @pyqtSlot()
    def set_placeholders(self):
        table_info = self.db_manager.get_info_about_table('Monuments')
        placeholders = {}

        for col in table_info:
            placeholders[col['name']] = col

        self.view.buttons_placeholders(placeholders)

    
    @pyqtSlot()
    def cancel_create(self):
        """Отмена изменение. Просто закрыть окно."""
        self.view.reject()  # Закрытие окна без изменение
    
    @pyqtSlot()
    def create_monument(self):
        data_to_insert = {
            'name': self.view.nameInsert.text(),
            'description': self.view.descriptionInsert.toPlainText(),
            'research_object': self.view.resObjInsert.text()
        }

        # --- ВАЛИДАЦИЯ ---
        is_valid, error_msg = self.validator.validate_create_method(data_to_insert)
        if not is_valid:
            QMessageBox.warning(self.view, "Ошибка валидации на уровне UI", error_msg)
            return

        # --- СОЗДАНИЕ ---
        try:
            success = self.db_manager.create_monument(data=data_to_insert)
            if success:
                self.view.accept()
        except Exception as e:
            QMessageBox.warning(self.view, "Ошибка валидации на уровне SQL", str(e))
        
            # raise

        



    
