import sys
import os
import folium
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class OSMMapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GIS Приложение")
        self.setGeometry(100, 100, 800, 600)

        # Создаем центральный виджет и макет
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)

        # Добавляем WebView для отображения карты
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)

        # Загружаем HTML-карту с растровым изображением
        folium_map = self.create_osm_map()
        map_url = QUrl.fromLocalFile(folium_map)  # Преобразуем путь в QUrl
        self.web_view.setUrl(map_url)

        self.setCentralWidget(central_widget)

    def create_osm_map(self):
        # Получаем текущую рабочую директорию, чтобы указать путь
        current_directory = os.path.dirname(os.path.abspath(__file__))
        
        # Создаем объект карты
        map_obj = folium.Map(location=[59.955, 30.305], zoom_start=15)  # Петропавловская крепость

        # Устанавливаем координаты для привязки растрового изображения
        image_bounds = [[59.950, 30.295], [59.960, 30.315]]  # Корректируем координаты под нужную область

        # Добавляем изображение на карту
        

        # Сохраняем карту с изображением в файл
        map_html = os.path.join(current_directory, 'osm_map_with_image.html')
        map_obj.save(map_html)
        
        return map_html

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OSMMapWindow()
    window.show()
    sys.exit(app.exec_())
