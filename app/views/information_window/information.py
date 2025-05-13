#файл подключает UI и больше ничего не делает. вся логика в Information_controller

import os
import sys
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi # Импортируем функцию для загрузки .ui файла
from PyQt5.QtCore import pyqtSlot, QObject
import config # здесь глобальные переменные хранятся
from views.information_window.about_authors import AboutAuthorsView
# Добавляем корневую директорию в sys.path
# Обеспечиваем корректный импорт при запуске из корня
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))) # при запуске приложения через main.py Ошибку при отсутствии этой строчки не выкидывает

class InformationView(QWidget):
    """класс отрисовывает ui файл 
    Args:
        QWidget (класс PyQt): оболочка для элементов интерфейса (окно где все расположено будет)
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        ui_path = os.path.join(config.UI_DIR, 'information_window.ui')
        loadUi(ui_path, self) # Загружаем интерфейс из .ui файла

class InformationController(QObject):
    """
    класс реализует всю логику которая происходит принажатии на пункт Information главного меню
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.view = InformationView()
        self.setup_connections()

    def setup_connections(self):
        self.view.AboutAuthorsButton.clicked.connect(self.show_about_authors)

    def show(self):
        self.view.show()

    @pyqtSlot() 
    def show_about_authors(self):
        self.dialog = AboutAuthorsView()
        self.dialog.exec_()  # модальное окно