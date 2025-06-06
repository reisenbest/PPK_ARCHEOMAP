
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

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

class UpdateMonumentView(QDialog, BaseView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_ui('update_monument_window.ui')

    def display_monument_data(self, monument_data):
        print(
            'peoverka ',monument_data)
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
        # Подключаем действия к кнопкам
        self.view.acceptUpdBtn.clicked.connect(self.update_monument)
        self.view.cancelBtn.clicked.connect(self.cancel_delete)  # Обработчик кнопки "Отмена
        self.view.addDelFilesBtn.clicked.connect(self.manage_files)  # Обработчик кнопки "добавиь\удалить файл"
    
    @pyqtSlot()
    def cancel_delete(self):
        """Отмена изменение. Просто закрыть окно."""
        self.view.reject()  # Закрытие окна без изменение
    
    @pyqtSlot()
    def manage_files(self):
        self.manage_files_controller.exec_dialog()
    
    
    @pyqtSlot()
    def update_monument(self):
        monument = self.monument_details.copy()  # копия, чтобы не портить оригинал

        old_name = self.monument_details['name']  # старое имя (до редактирования)
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
            QMessageBox.warning(self.view, "Ошибка валидации на уровне UI", error_msg)
            return

        try:
            success = self.db_manager.monuments.update_monument_by_id(
                monument_id=monument['monument_id'],
                monument=monument
            )

            if success:
                # --- Переименование папки, если имя изменилось ---
                old_safe_name = re.sub(r'[^\w\-_ ]', '_', old_name.strip())
                new_safe_name = re.sub(r'[^\w\-_ ]', '_', new_name.strip())

                if old_safe_name != new_safe_name:
                    old_path = os.path.join(config.DATA_STORAGE_DIR, old_safe_name)
                    new_path = os.path.join(config.DATA_STORAGE_DIR, new_safe_name)

                    try:
                        if os.path.exists(old_path):
                            os.rename(old_path, new_path)
                            print(f"Папка переименована: {old_path} → {new_path}")
                        elif not os.path.exists(new_path):
                            # Если старая папка отсутствует, а новая ещё не существует — создаём
                            os.makedirs(new_path)
                            print(f"Создана новая папка памятника: {new_path}")
                    except Exception as folder_err:
                        QMessageBox.warning(self.view, "Ошибка переименования папки", str(folder_err))

                self.view.accept()
            else:
                QMessageBox.warning(self.view, "Ошибка", "Не удалось обновить памятник.")

        except Exception as e:
            QMessageBox.critical(self.view, "Ошибка", f"Произошла ошибка при обновлении:\n{e}")
            


    
