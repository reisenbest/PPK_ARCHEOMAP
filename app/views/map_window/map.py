
import os
import sys
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi # Импортируем функцию для загрузки .ui файла
import config # здесь глобальные переменные хранятся
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, pyqtSlot, QObject
from utils.base_classes import BaseView
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import pyqtSlot
# Добавляем корневую директорию в sys.path
# Обеспечиваем корректный импорт при запуске из корня


from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings

class MapView(QWidget, BaseView):
    def __init__(self, bridge_object, parent=None):  # <-- получаем MapBridge извне
        super().__init__(parent)
        self.load_ui('map_window.ui')

        self.web_view: QWebEngineView = self.findChild(QWebEngineView, "MapContainer")

        
        # Создаем канал и подключаем bridge
        self.channel = QWebChannel()
        self.channel.registerObject("bridge", bridge_object)  # "bridge" — имя в JS
        self.web_view.page().setWebChannel(self.channel)

        # Загружаем HTML
        html_path = os.path.join(config.MAP_DIR, 'OSM/index.html')
        if os.path.exists(html_path):
            local_url = QUrl.fromLocalFile(os.path.abspath(html_path))
            self.web_view.load(local_url)
        else:
            print(f"[ОШИБКА] HTML-файл карты не найден: {html_path}")



class MapBridge(QObject):
    def __init__(self, db_manager, parent=None):  # <-- получаем MapBridge извне
        super().__init__(parent)
        self.db_manager = db_manager
    @pyqtSlot(result='QVariant')
    def get_monuments_markers(self):
        monuments = self.db_manager.get_monuments()
        data = []
        for monument in monuments:
            data.append({'lat': monument['latitude'],
                         'lng': monument['longitude'],
                         'label': monument['research_object']})
            print(monument)
        # print(monuments)
        # Координаты двух бастионов Петропавловской крепости
        return data
    

class MapController(QObject):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.bridge = MapBridge(self.db_manager)  # создаём bridge
        self.view = MapView(self.bridge)  # передаём его в MapView

    def show(self):
        self.view.show()

    def setup_connections(self):
        pass
