
import os
import sys
import config
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot, QObject
from PyQt5.uic import loadUi



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

class CreateMonumentView(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        ui_path = os.path.join(config.UI_DIR, 'create_monument_window.ui')
        loadUi(ui_path, self)

class CreateMonumentController(QObject):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.view = CreateMonumentView()
        self.db_manager = db_manager
        self.setup_connections()

    def show(self):
        self.view.show()

    def setup_connections(self):
        """Настройка подключения кнопок."""
        # Подключаем действия к кнопкам
        self.view.createBtn.clicked.connect(self.create_monument)
        self.view.cancelBtn.clicked.connect(self.cancel_create)  # Обработчик кнопки "Отмена
    
    @pyqtSlot()
    def cancel_create(self):
        """Отмена изменение. Просто закрыть окно."""
        self.view.reject()  # Закрытие окна без изменение
    
    @pyqtSlot()
    def create_monument(self):
        print('создание памятника заглушка')
        # monument = self.monument_details

        # monument['name'] = self.view.nameEdit.text()
        # monument['description'] = self.view.descriptionEdit.toPlainText()
        # monument['research_object'] = self.view.resObjEdit.text()

        # self.db_manager.update_monument_by_id(monument_id=monument['monument_id'],
        #                                       monument=monument)
        
        self.view.accept()  # Закрытие окна после успешного изменение
        
        # monument_id = self.monument_details['monument_id']
        # self.db_manager.update_monument_by_id(monument_id)  # Удаляем памятник
        # self.view.accept()  # Закрытие окна после успешного удаления


    
