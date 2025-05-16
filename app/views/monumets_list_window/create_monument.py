
import os
import sys
import config
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot, QObject
from PyQt5.uic import loadUi
import json


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

class CreateMonumentView(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        ui_path = os.path.join(config.UI_DIR, 'create_monument_window.ui')
        loadUi(ui_path, self)
    
    def buttons_placeholders(self, table_info: dict):
        name_placeholder = f'имя столбца: {table_info['name']['name']}, тип: {table_info['name']['type']}          '
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
        data_to_insert = {}

        data_to_insert['name'] = self.view.nameInsert.text()
        data_to_insert['description'] = self.view.descriptionInsert.toPlainText()
        data_to_insert['research_object'] = self.view.resObjInsert.text()
        
        try:
            success = self.db_manager.create_monument(data=data_to_insert)
            if success:
                self.view.accept()
            else:
                QMessageBox.warning(self.view, "Ошибка", "Не удалось создать памятник.")
        except Exception as e:
            QMessageBox.critical(self.view, "Ошибка", f"Произошла ошибка при создании:\n{e}")
        



    
