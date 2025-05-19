
import os
import sys
import config
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot, QObject
from PyQt5.uic import loadUi
from utils.base_classes import BaseView
from utils.validate_manager import ValidateUILevelManager   

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

class UpdateMonumentView(QDialog, BaseView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_ui('update_monument_window.ui')

    def display_monument_data(self, monument_data):
        self.nameEdit.setText(monument_data['name'])
        self.descriptionEdit.setText(monument_data['description'])
        self.resObjEdit.setText(monument_data['research_object'])


        

class UpdateMonumentController(QObject):
    def __init__(self, monument_details, db_manager, parent=None):
        super().__init__(parent)
        self.view = UpdateMonumentView()
        self.db_manager = db_manager
        self.monument_details = monument_details
        self.view.display_monument_data(monument_details)  # Заполняем окно данными
        self.setup_connections()
        self.validator = ValidateUILevelManager(db_manager=self.db_manager)

    def show(self):
        self.view.show()

    def setup_connections(self):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
        """Настройка подключения кнопок."""
        # Подключаем действия к кнопкам
        self.view.acceptUpdBtn.clicked.connect(self.update_monument)
        self.view.cancelBtn.clicked.connect(self.cancel_delete)  # Обработчик кнопки "Отмена
    
    @pyqtSlot()
    def cancel_delete(self):
        """Отмена изменение. Просто закрыть окно."""
        self.view.reject()  # Закрытие окна без изменение
    
    @pyqtSlot()
    def update_monument(self):
        
        monument = self.monument_details

        monument['name'] = self.view.nameEdit.text()
        monument['description'] = self.view.descriptionEdit.toPlainText()
        monument['research_object'] = self.view.resObjEdit.text()


        is_valid, error_msg = self.validator.validate_create_method(monument)
        if not is_valid:
            QMessageBox.warning(self.view, "Ошибка валидации на уровне UI", error_msg)
            return
        

        try:
            success = self.db_manager.update_monument_by_id(monument_id=monument['monument_id'],
                                              monument=monument)
            if success:
                self.view.accept()  # обновление успешно — закрыть окно и вернуть Accepted
            else:
                QMessageBox.warning(self.view, "Ошибка валидации на уровне sql", "Не удалось обновить памятник.")

        except Exception as e:
             QMessageBox.critical(self.view, "Ошибка валидации на уровне sql", f"Произошла ошибка при обновлении:\n{e}")
        


    
