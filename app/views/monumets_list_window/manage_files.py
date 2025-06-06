import os
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from utils.base_classes import BaseView
from PyQt5.QtCore import QObject
import os
from PyQt5.QtCore import QObject, Qt
from PyQt5.QtWidgets import QFileDialog, QInputDialog, QMessageBox, QTableWidgetItem
import shutil
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import config
from PyQt5.QtSql import QSqlQuery
import re
from database.db_main_connection import DataBaseFilesTableManager


class ManageFilesView(QDialog, BaseView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_ui('manage_files_window.ui')  # путь должен быть правильный

        
class ManageFilesController(QObject):
    def __init__(self, db_manager, monument_id, parent=None):
        super().__init__(parent)
        self.view = ManageFilesView(parent)
        self.db_manager = db_manager
        self.monument_id = monument_id
        self.selected_files = []

        self.setup_connections()
        self.load_files()

    def setup_connections(self):
        self.view.addFileBtn.clicked.connect(self.browse_file)
        self.view.deleteFileBtn.clicked.connect(self.delete_selected_files)

    def exec_dialog(self):
        self.view.exec_()

    def load_files(self):
        try:
            files = self.db_manager.files_table.get_files_for_monument_by_monument_id(self.monument_id)
        except Exception as e:
            QMessageBox.critical(self.view, "Ошибка загрузки", str(e))
            return

        model = QStandardItemModel(len(files), 4)
        model.setHorizontalHeaderLabels(["ID", "Имя файла", "Тип", "Описание"])
        
        for row_idx, file_data in enumerate(files):
            print(file_data)
            model.setItem(row_idx, 0, QStandardItem(str(file_data["file_id"])))
            model.setItem(row_idx, 1, QStandardItem(file_data["file_path"]))
            model.setItem(row_idx, 2, QStandardItem(file_data.get("file_type", "")))
            model.setItem(row_idx, 3, QStandardItem(file_data.get("file_description", "")))

        self.view.filesTableView.setModel(model)
        self.view.filesTableView.resizeColumnsToContents()
        self.model = model  # сохраним модель, если потом нужно удаление

    # @pyqtSlot()
    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self.view, "Выберите файл", "", "Все файлы (*.*)")
        if not file_path:
            return

        description, ok = QInputDialog.getText(self.view, "Описание файла", f"Введите описание для:\n{os.path.basename(file_path)}")
        if not ok:
            return

        file_type, ok_type = QInputDialog.getText(self.view, "Тип файла", f"Введите тип для:\n{os.path.basename(file_path)} (например: pdf, jpg, obj, txt...)")
        if not ok_type:
            return

        # Получаем данные памятника по ID
        monument_record = self.db_manager.monuments_table.get_monument_by_id(self.monument_id)
        if not monument_record:
            QMessageBox.critical(self.view, "Ошибка", "Не удалось получить данные памятника из базы")
            return

        monument_name_raw = monument_record.get('name', '')
        if not monument_name_raw:
            QMessageBox.critical(self.view, "Ошибка", "Имя памятника не найдено в данных")
            return

        # Делаем безопасное имя для папки
        safe_name = re.sub(r'[^\w\-_ ]', '_', monument_name_raw.strip())
        monument_folder = os.path.join(config.DATA_STORAGE_DIR, safe_name)

        # Обработка полного пути и имени файла
        original_filename = os.path.basename(file_path)
        safe_filename = re.sub(r'[^\w\-. ]', '_', original_filename)  # точки и дефисы оставляем

        # Защита от спецсимволов во всём пути (не только имя файла!)
        safe_target_path = os.path.join(monument_folder, safe_filename)

        try:
            shutil.copy(file_path, safe_target_path)
        except Exception as e:
            QMessageBox.critical(self.view, "Ошибка копирования файла", f"Не удалось скопировать файл:\n{str(e)}")
            return

        # Получить относительный путь (безопасно)
        relative_path = os.path.relpath(safe_target_path, config.DATA_STORAGE_DIR)

        # Очистка дополнительных полей
        cleaned_description = re.sub(r'[^\wа-яА-ЯёЁ0-9\-.,()!? ]', '_', description.strip())  # русский + цифры + знаки
        cleaned_file_type = re.sub(r'[^\w\-]', '_', file_type.strip())

        try:
            self.db_manager.files_table.add_file(relative_path, cleaned_file_type, cleaned_description, self.monument_id)
        except Exception as e:
            QMessageBox.critical(self.view, "Ошибка при добавлении файла в БД", str(e))
            return

        self.load_files()

    def delete_selected_files(self):
        table = self.view.filesTableView
        model = table.model()
        selected_rows = set(index.row() for index in table.selectedIndexes())

        if not selected_rows:
            QMessageBox.information(self.view, "Удаление", "Выберите хотя бы одну строку для удаления.")
            return

        confirm = QMessageBox.question(
            self.view,
            "Подтвердите удаление",
            "Вы уверены, что хотите удалить выбранные файлы?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm != QMessageBox.Yes:
            return

        # Получаем имя памятника для построения пути
        monument_record = self.db_manager.monuments_table.get_monument_by_id(self.monument_id)
        if not monument_record:
            QMessageBox.critical(self.view, "Ошибка", "Не удалось получить данные памятника из базы")
            return

        monument_name_raw = monument_record.get('name', '')
        if not monument_name_raw:
            QMessageBox.critical(self.view, "Ошибка", "Имя памятника не найдено в данных")
            return

        safe_name = re.sub(r'[^\w\-_ ]', '_', monument_name_raw.strip())
        monument_folder = os.path.join(config.DATA_STORAGE_DIR, safe_name)

        for row in sorted(selected_rows, reverse=True):
            file_id_index = model.index(row, 0)
            file_path_index = model.index(row, 1)  # путь или имя файла в столбце 1

            file_id = int(model.data(file_id_index))
            relative_path = model.data(file_path_index)  # относительный путь из БД

            full_path = os.path.join(config.DATA_STORAGE_DIR, relative_path)

            if os.path.exists(full_path):
                try:
                    os.remove(full_path)
                except Exception as e:
                    QMessageBox.warning(self.view, "Ошибка удаления файла", f"Не удалось удалить файл:\n{full_path}\n{e}")
                    continue

            try:
                self.db_manager.files_table.delete_file_by_id(file_id)
            except Exception as e:
                QMessageBox.warning(self.view, "Ошибка удаления записи из базы", str(e))

        self.load_files()

    


    
