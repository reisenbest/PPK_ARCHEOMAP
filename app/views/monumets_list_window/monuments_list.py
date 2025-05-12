import os
import sys
from PyQt5.QtWidgets import QWidget, QListWidgetItem, QListWidget
from PyQt5.uic import loadUi
import config
from database.db_main_connection import DBHelper  # Импортируем наш помощник для работы с БД

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))  # Путь до проекта


class MonumentListView(QWidget):
    """Отображение списка памятников."""
    def __init__(self, parent=None):
        super().__init__(parent)
        ui_path = os.path.join(config.UI_DIR, 'monuments_list_window.ui')
        loadUi(ui_path, self)  # Загружаем интерфейс из .ui файла

        # Инициализируем список памятников
        self.monument_list_widget = self.findChild(QListWidget, "MonumentslistWidget")  # Предполагаем, что это QListWidget в .ui файле

    def display_monuments(self, monuments):
        """Отображение памятников в списке."""
        self.monument_list_widget.clear()  # Очищаем список перед добавлением новых данных
        for monument in monuments:
            item = QListWidgetItem(monument[1])  # monument[1] — это, например, название памятника
            item.setData(1, monument[0])  # Сохраняем ID памятника как данные элемента
            self.monument_list_widget.addItem(item)


class MonumentListController:
    """Логика работы с памятниками."""

    def __init__(self):
        self.view = MonumentListView()
        self.db_helper = DBHelper(os.path.join(config.DATABASE_DIR, 'database.db'))  # Создаем экземпляр DBHelper
        self.setup_connections()

    def show(self):
        self.view.show()

    def setup_connections(self):
        """Подключаем события."""
        self.view.monument_list_widget.itemClicked.connect(self.on_monument_click)

        # Загружаем список памятников из базы данных
        monuments = self.db_helper.get_monuments()
        self.view.display_monuments(monuments)

    def on_monument_click(self, item):
        """Обработка клика по элементу в списке."""
        monument_id = item.data(1)  # Получаем ID памятника
        monument_details = self.db_helper.get_monument_details(monument_id)

        # Показываем информацию о памятнике
        self.show_monument_details(monument_details)

    def show_monument_details(self, details):
        """Отображаем информацию о памятнике."""
        # Реализуйте отображение данных в нужном окне или компоненте
        print(details)