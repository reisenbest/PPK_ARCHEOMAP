import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi  # Импортируем функцию для загрузки .ui файла
import os
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

# Добавляем корневую директорию в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # при запуске приложения через main.py Ошибку при отсутствии этой строчки не выкидывает

import config  # Импортируем конфигурацию

ui_file_path = os.path.join(config.UI_DIR, 'main_menu.ui')

class MainMenuView(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi(ui_file_path, self)  # Загружаем интерфейс из .ui файла