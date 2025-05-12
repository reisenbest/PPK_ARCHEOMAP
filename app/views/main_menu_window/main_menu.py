import os
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi  # Импортируем функцию для загрузки .ui файла
from PyQt5.QtCore import pyqtSlot, QObject

# Добавляем корневую директорию в sys.path
# Обеспечиваем корректный импорт при запуске из корня
# при запуске приложения через main.py Ошибку при отсутствии этой строчки не выкидывает
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', )))
import config
from views.map_window.map import MapController
from views.information_window.information import InformationController
from views.monumets_list_window.monuments_list import MonumentListController


class MainMenuView(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        ui_path = os.path.join(config.UI_DIR, 'main_menu_window.ui')
        loadUi(ui_path, self)  # Загружаем интерфейс из .ui файла


class MainMenuController(QObject):  # Наследуем от QObject для работы с сигналами и слотами
    def __init__(self, parent=None):
        super().__init__(parent)
        self.view = MainMenuView()
        self.setup_connections()

    def setup_connections(self):
        self.view.MenuExitButton.clicked.connect(self.exit_app)
        self.view.MenuInfoButton.clicked.connect(self.open_information_window)
        self.view.MenuMapButton.clicked.connect(self.open_map_window)
        self.view.MenuMonumentsListButton.clicked.connect(self.open_monuments_list_window)

    def show(self):
        self.view.show()

    @pyqtSlot()  # Здесь все правильно: слот для выхода
    def exit_app(self):
        QApplication.quit()

    @pyqtSlot()  # Слот для открытия окна информации
    def open_information_window(self):
        self.info_controller = InformationController()
        self.info_controller.show()

    @pyqtSlot()  # Слот для открытия карты
    def open_map_window(self):
        self.map_controller = MapController()
        self.map_controller.show()

    @pyqtSlot()  # Слот для открытия списка памятников
    def open_monuments_list_window(self):
        self.monuments_list_controller = MonumentListController()
        self.monuments_list_controller.show()
