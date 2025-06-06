
import os
import sys
import re  # для очистки имени
import config
import shutil
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot, QObject
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QInputDialog
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

        print('table info', table_info)
        
        self.nameInsert.setPlaceholderText(name_placeholder)
        self.descriptionInsert.setPlaceholderText(description_placeholder)
        self.resObjInsert.setPlaceholderText(json.dumps(table_info['research_object']))
        self.filePathInsert.setPlaceholderText('file_path_placeholder')
    

class CreateMonumentController(QObject):

    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.view = CreateMonumentView()
        self.db_manager = db_manager
        self.setup_connections()
        self.set_placeholders()
        self.validator = ValidateUILevelManager(db_manager=self.db_manager)
        self.selected_files = []  # список словарей с путём и описанием

    def show(self):
        self.view.show()

    def setup_connections(self):
        """Настройка подключения кнопок."""
        # Подключаем действия к кнопкам
        self.view.createBtn.clicked.connect(self.create_monument)
        self.view.cancelBtn.clicked.connect(self.cancel_create)  # Обработчик кнопки "Отмена
        self.view.browseBtn.clicked.connect(self.browse_file) # загрузить файл
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
    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self.view, "Выберите файл", "", "Все файлы (*.*)")
        if not file_path:
            return

        # Ввод описания файла
        description, ok = QInputDialog.getText(self.view, "Описание файла", f"Введите описание для:\n{os.path.basename(file_path)}")
        if not ok:
            return

        # Ввод типа файла
        file_type, ok_type = QInputDialog.getText(self.view, "Тип файла", f"Введите тип для:\n{os.path.basename(file_path)} (например: pdf, jpg, obj, txt...)")
        if not ok_type:
            return

        self.selected_files.append({
            'path': file_path,
            'description': description.strip(),
            'file_type': file_type.strip()
        })

        # Обновить поле отображения файлов
        filenames = [os.path.basename(f['path']) for f in self.selected_files]
        self.view.filePathInsert.setText("; ".join(filenames))
    
    @pyqtSlot()
    def create_monument(self):
        raw_name = self.view.nameInsert.text().strip()
        safe_name = re.sub(r'[^\w\-_ ]', '_', raw_name)

        raw_file_path = self.view.filePathInsert.text().strip()

        # Сначала создать папку
        monument_path = os.path.join(config.DATA_STORAGE_DIR, safe_name)
        try:
            os.makedirs(monument_path, exist_ok=True)
        except Exception as folder_err:
            QMessageBox.warning(self.view, "Ошибка при создании папки", str(folder_err))
            return

        # Скопировать файл
        files_data = []

        for file_entry in self.selected_files:
            file_path = file_entry['path']
            description = file_entry['description']

            if os.path.exists(file_path):
                try:
                    filename = os.path.basename(file_path)
                    target_path = os.path.join(monument_path, filename)
                    shutil.copy(file_path, target_path)

                    relative_path = os.path.relpath(target_path, config.DATA_STORAGE_DIR)

                    files_data.append({
                        'file_path': relative_path,
                        'file_type': file_entry['file_type'],
                        'file_description': description
                    })
                except Exception as copy_err:
                    QMessageBox.warning(self.view, "Ошибка при копировании файла", f"{file_path}\n{str(copy_err)}")
                    return

        # Собрать финальный словарь для вставки
        data_to_insert = {
            'name': safe_name,
            'description': self.view.descriptionInsert.toPlainText(),
            'research_object': self.view.resObjInsert.text(),
            'latitude': self.view.latitudeInsert.value(),
            'longitude': self.view.longitudeInsert.value(),
            'note': self.view.coordNoteInsert.toPlainText(),
        }

        if files_data:
            data_to_insert['files'] = files_data

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
            QMessageBox.warning(self.view, "Ошибка при создании памятника", str(e))
            



    
