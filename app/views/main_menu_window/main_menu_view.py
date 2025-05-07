# подключает UI
import os
import sys
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi # Импортируем функцию для загрузки .ui файла
import config
# Добавляем корневую директорию в sys.path
# Обеспечиваем корректный импорт при запуске из корня
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))) # при запуске приложения через main.py Ошибку при отсутствии этой строчки не выкидывает

class MainMenuView(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(config.UI_DIR, 'main_menu.ui')
        loadUi(ui_path, self) # Загружаем интерфейс из .ui файла