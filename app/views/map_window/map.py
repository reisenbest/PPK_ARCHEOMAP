
import os
import sys
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi # Импортируем функцию для загрузки .ui файла
import config # здесь глобальные переменные хранятся
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, pyqtSlot, QObject
from utils.base_classes import BaseView
# Добавляем корневую директорию в sys.path
# Обеспечиваем корректный импорт при запуске из корня


class MapView(QWidget, BaseView):
    def __init__(self):
        super().__init__()
        self.load_ui('map_window.ui')

        # Получаем QWebEngineView по имени из .ui
        self.web_view: QWebEngineView = self.findChild(QWebEngineView, "MapContainer")

        # Загружаем локальный HTML-файл с картой
        html_path = os.path.join(config.MAP_DIR, 'OSM/index.html')  # Путь к твоей карте
        if os.path.exists(html_path):
            local_url = QUrl.fromLocalFile(os.path.abspath(html_path))
            self.web_view.load(local_url)
        else:
            print(f"[ОШИБКА] HTML-файл карты не найден: {html_path}")

class MapController(QObject):
    """
    класс реализует всю логику которая происходит принажатии на пункт Information главного меню
    """
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.view = MapView()
        self.db_manager = db_manager
        self.setup_connections()

    def show(self):
        self.view.show()
    
    def setup_connections(self):
        pass
