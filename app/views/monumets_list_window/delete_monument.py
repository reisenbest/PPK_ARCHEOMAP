import os
import sys
import config
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot, QObject
from PyQt5.uic import loadUi
from utils.base_classes import BaseView
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..', '..')))


class DeleteMonumentView(QDialog, BaseView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_ui('delete_monument_window.ui')



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
        try:
            success = self.db_manager.delete_monument_by_id(monument_id)
            if success:
                self.view.accept()  # Удаление успешно — закрыть окно и вернуть Accepted
            else:
                QMessageBox.warning(self.view, "Ошибка",
                                    "Не удалось удалить памятник.")
        except Exception as e:
            QMessageBox.critical(self.view, "Ошибка",
                                 f"Произошла ошибка при удалении:\n{e}")
            # Окно не закрывается, пользователь может попробовать снова

    @pyqtSlot()
    def cancel_delete(self):
        """Отмена удаления. Просто закрыть окно."""
        self.view.reject()  # Закрытие окна без удаления

    def setup_connections(self):
        """Настройка подключения кнопок."""
        # Подключаем действия к кнопкам
        self.view.delMonumentBtn.clicked.connect(self.delete_monument)
        self.view.cancelDelMonumentBtn.clicked.connect(
            self.cancel_delete)  # Обработчик кнопки "Отмена"
