import os
import sys
import re
import config
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot, QObject
from PyQt5.uic import loadUi
from utils.base_classes import BaseView
from utils.validate_manager import ValidateUILevelManager
from views.monumets_list_window.manage_files import ManageFilesController
import shutil

sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..', '..')))


class UpdateMonumentView(QDialog, BaseView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_ui('update_monument_window.ui')

    def display_monument_data(self, monument_data):
        print('peoverka ', monument_data)
        self.nameEdit.setText(monument_data['name'])
        self.descriptionEdit.setText(monument_data['description'])
        self.resObjEdit.setText(monument_data['research_object'])
        self.latitudeEdit.setValue(monument_data['latitude'])
        self.longitudeEdit.setValue(monument_data['longitude'])
        self.coordNoteEdit.setText(monument_data['note'])


class UpdateMonumentController(QObject):
    def __init__(self, monument_details, db_manager, parent=None):
        super().__init__(parent)
        self.view = UpdateMonumentView()
        self.db_manager = db_manager
        self.monument_details = monument_details
        self.view.display_monument_data(monument_data=monument_details)
        self.setup_connections()
        self.validator = ValidateUILevelManager(db_manager=self.db_manager)
        self.manage_files_controller = ManageFilesController(
            db_manager=self.db_manager,
            monument_id=self.monument_details['monument_id'],
            parent=self.view
        )

    def show(self):
        self.view.show()

    def setup_connections(self):
        """Настройка подключения кнопок."""
        self.view.acceptUpdBtn.clicked.connect(self.update_monument)
        self.view.cancelBtn.clicked.connect(self.cancel_delete)
        self.view.addDelFilesBtn.clicked.connect(self.manage_files)

    @pyqtSlot()
    def cancel_delete(self):
        """Отмена изменения. Просто закрыть окно."""
        self.view.reject()

    @pyqtSlot()
    def manage_files(self):
        self.manage_files_controller.exec_dialog()

    @pyqtSlot()
    def update_monument(self):
        monument = self.monument_details.copy()  # копия, чтобы не портить оригинал

        # старое имя (до редактирования)
        old_name = self.monument_details['name']
        new_name = self.view.nameEdit.text()      # новое имя (после редактирования)

        # Обновляем поля памятника
        monument['name'] = new_name
        monument['description'] = self.view.descriptionEdit.toPlainText()
        monument['research_object'] = self.view.resObjEdit.text()
        monument['latitude'] = self.view.latitudeEdit.value()
        monument['longitude'] = self.view.longitudeEdit.value()
        monument['note'] = self.view.coordNoteEdit.toPlainText()

        # --- Валидация ---
        is_valid, error_msg = self.validator.validate_create_method(monument)
        if not is_valid:
            QMessageBox.warning(
                self.view, "Ошибка валидации на уровне UI", error_msg)
            return

        try:
            success = self.db_manager.monuments_table.update_monument_by_id(
                monument_id=monument['monument_id'],
                monument=monument
            )

            if success:
                # --- Переименование папки, если имя изменилось ---
                old_safe_name = re.sub(r'[^\w\-_ ]', '_', old_name.strip())
                new_safe_name = re.sub(r'[^\w\-_ ]', '_', new_name.strip())

                if old_safe_name != new_safe_name:
                    old_path = os.path.join(
                        config.DATA_STORAGE_DIR, old_safe_name)
                    new_path = os.path.join(
                        config.DATA_STORAGE_DIR, new_safe_name)

                    try:
                        if os.path.exists(old_path):
                            os.rename(old_path, new_path)
                            print(
                                f"Папка переименована: {old_path} → {new_path}")
                        elif not os.path.exists(new_path):
                            os.makedirs(new_path)
                            print(f"Создана новая папка памятника: {new_path}")
                    except Exception as folder_err:
                        QMessageBox.warning(
                            self.view, "Ошибка переименования папки", str(folder_err))
                        return

                    # Обновляем пути файлов в базе данных
                    self.update_file_paths(
                        monument['monument_id'], old_safe_name, new_safe_name)

                self.view.accept()
            else:
                QMessageBox.warning(self.view, "Ошибка",
                                    "Не удалось обновить памятник.")

        except Exception as e:
            QMessageBox.critical(self.view, "Ошибка",
                                 f"Произошла ошибка при обновлении:\n{e}")

    def update_file_paths(self, monument_id: int, old_folder_name: str, new_folder_name: str):
        files = self.db_manager.files_table.get_files_for_monument_by_monument_id(
            monument_id)

        for file in files:
            old_rel_path = file['file_path']  # например, OLDNAME\abc.jpg

            # Заменим только первую часть пути (название папки-памятника)
            parts = old_rel_path.split(os.sep)
            if parts[0] != old_folder_name:
                print(
                    f"Пропущен файл — не совпадает имя папки: {old_rel_path}")
                continue

            parts[0] = new_folder_name  # заменяем на новое имя
            new_rel_path = os.path.join(*parts)

            try:
                self.db_manager.files_table.update_file_paths(
                    file['file_id'], new_rel_path)
            except Exception as e:
                print(
                    f"Ошибка обновления пути в БД для файла ID {file['file_id']}: {e}")
