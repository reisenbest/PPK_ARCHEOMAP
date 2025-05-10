# подключает UI



import os
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi  # Импортируем функцию для загрузки .ui файла


# Добавляем корневую директорию в sys.path
# Обеспечиваем корректный импорт при запуске из корня
# при запуске приложения через main.py Ошибку при отсутствии этой строчки не выкидывает
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', )))
import config
from views.map_window.map import MapController
from views.information_window.information import InformationController


class MainMenuView(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(config.UI_DIR, 'main_menu_window.ui')
        loadUi(ui_path, self)  # Загружаем интерфейс из .ui файла


class MainMenuController:
    def __init__(self):
        self.view = MainMenuView()
        self.setup_connections()

    def setup_connections(self):
        self.view.MenuExitButton.clicked.connect(self.exit_app)
        self.view.MenuInfoButton.clicked.connect(self.open_information_window)
        self.view.MenuMapButton.clicked.connect(self.open_map_window)

    def show(self):
        self.view.show()

    def exit_app(self):
        QApplication.quit()

    def open_information_window(self):
        self.info_controller = InformationController()
        self.info_controller.show()
    

    def open_map_window(self):
        self.map_controller = MapController()
        self.map_controller.show()
