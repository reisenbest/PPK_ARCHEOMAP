# Общее окно где отображается кликабельный список памятников. при клике отображается каждый конкретный

#файл подключает UI и больше ничего не делает. вся логика в Information_controller

import os
import sys
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi # Импортируем функцию для загрузки .ui файла
import config # здесь глобальные переменные хранятся
# Добавляем корневую директорию в sys.path
# Обеспечиваем корректный импорт при запуске из корня
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))) # при запуске приложения через main.py Ошибку при отсутствии этой строчки не выкидывает

class MonumentListView(QWidget):
    """класс отрисовывает ui файл 
    Args:
        QWidget (класс PyQt): оболочка для элементов интерфейса (окно где все расположено будет)
    """
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(config.UI_DIR, 'monuments_list_window.ui')
        loadUi(ui_path, self) # Загружаем интерфейс из .ui файла

class MonumentListController:
    """
    класс реализует всю логику которая происходит принажатии на пункт Monument List n главного меню
    """
    def __init__(self):
        self.view = MonumentListView()
        self.setup_connections()

    def show(self):
        self.view.show()

    def setup_connections(self):
        pass