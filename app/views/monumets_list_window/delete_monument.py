import os
import sys
import config
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot, QObject
from PyQt5.uic import loadUi

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

class DeleteMonumentView(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        ui_path = os.path.join(config.UI_DIR, 'delete_monument_window.ui')
        loadUi(ui_path, self)  # Загружаем UI

class DeleteMonumentController(QObject):
    def __init__(self, monument_details, db_manager, parent=None):
        super().__init__(parent)
        self.view = DeleteMonumentView()
        self.monument_details = monument_details  # Данные памятника для удаления
        self.db_manager = db_manager  # Ссылка на менеджер БД
        self.setup_connections()  # Настройка подключений (кнопки)

    def show(self):
        """Отображаем окно с данными памятника."""
        self.view.show()

    def delete_monument(self):
        """Удаление памятника из базы данных по ID."""
        monument_id = self.monument_details['monument_id']
        self.db_manager.delete_monument_by_id(monument_id)  # Удаляем памятник
        self.view.accept()  # Закрытие окна после успешного удаления

    @pyqtSlot()
    def cancel_delete(self):
        """Отмена удаления. Просто закрыть окно."""
        self.view.reject()  # Закрытие окна без удаления

    def setup_connections(self):
        """Настройка подключения кнопок."""
        # Подключаем действия к кнопкам
        self.view.delMonumentBtn.clicked.connect(self.delete_monument)
        self.view.cancelDelMonumentBtn.clicked.connect(self.cancel_delete)  # Обработчик кнопки "Отмена"
