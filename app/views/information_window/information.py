#файл подключает UI и больше ничего не делает. вся логика в Information_controller

import os
import sys
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi # Импортируем функцию для загрузки .ui файла
from PyQt5.QtCore import pyqtSlot, QObject
import config # здесь глобальные переменные хранятся
from views.information_window.about_authors import AboutAuthorsController
from utils.base_classes import BaseView
# Добавляем корневую директорию в sys.path
# Обеспечиваем корректный импорт при запуске из корня
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))) # при запуске приложения через main.py Ошибку при отсутствии этой строчки не выкидывает


class InformationView(QWidget, BaseView):
    """класс отрисовывает ui файл 
    Args:
        QWidget (класс PyQt): оболочка для элементов интерфейса (окно где все расположено будет)
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_ui('information_window.ui')

class InformationController(QObject):
    """
    класс реализует всю логику которая происходит принажатии на пункт Information главного меню
    """
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.view = InformationView()
        self.db_manager = db_manager
        self.setup_connections()

    def setup_connections(self):
        self.view.AboutAuthorsButton.clicked.connect(self.show_about_authors)

    def show(self):
        self.view.show()

    @pyqtSlot() 
    def show_about_authors(self):
        self.dialog = AboutAuthorsController()
        self.dialog.view.exec_()  # вызываем exec_() на объекте QDialog