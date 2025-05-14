import os
import sys
from PyQt5.QtWidgets import QWidget, QListWidgetItem, QListWidget
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, QObject
import config
from database.db_main_connection import DataBaseManager  # Импортируем наш помощник для работы с БД
from views.monumets_list_window.read_monument import ReadMonumentController
from views.monumets_list_window.delete_monument import DeleteMonumentController

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
            item = QListWidgetItem(monument['name'])  # Название памятника
            item.setData(1, monument['monument_id'])  # ID памятника
            self.monument_list_widget.addItem(item)


class MonumentListController(QObject):
    """Логика работы с памятниками."""

    def __init__(self, db_manager,  parent=None):
        super().__init__(parent)
        self.view = MonumentListView()
        self.db_manager = db_manager
        self.setup_connections()
        self.current_monument_details = None  # Будет хранить данные выбранного памятника

    def show(self):
        self.view.show()

    def setup_connections(self):
        """Подключаем события."""
        self.view.readMonumentBtn.setEnabled(False)
        self.view.createMonumentBtn.setEnabled(False)
        self.view.updateMonumentBtn.setEnabled(False)
        self.view.deleteMonumentBtn.setEnabled(False)
        
        self.view.monument_list_widget.itemSelectionChanged.connect(self.update_buttons_state)
        self.view.monument_list_widget.itemClicked.connect(self.on_monument_click)
        
        # TODO Сделать отдлеьным методом в классе обработчика бд и повесить его на кнопки
        # Загружаем список памятников из базы данных ()
        monuments = self.db_manager.get_monuments()
        self.view.display_monuments(monuments)

        self.view.readMonumentBtn.clicked.connect(self.show_read_monument)
        self.view.deleteMonumentBtn.clicked.connect(self.delete_monument)
        self.view.refreshBtn.clicked.connect(self.refresh_data)

    @pyqtSlot()
    def show_read_monument(self):
        self.read_monument = ReadMonumentController(self.monument_details)
        self.read_monument.show()
    
    @pyqtSlot()
    def delete_monument(self):
        self.delete_monument = DeleteMonumentController(monument_details=self.monument_details,
                                                        db_manager=self.db_manager)
        self.delete_monument.show()
    
    @pyqtSlot()
    def refresh_data(self):
        """Обновляет список памятников."""
        monuments = self.db_manager.get_monuments()  # Получаем свежие данные
        self.view.display_monuments(monuments)       # Отображаем их
        self.view.readMonumentBtn.setEnabled(False)  # Сбрасываем состояние кнопок
        self.view.createMonumentBtn.setEnabled(False)
        self.view.updateMonumentBtn.setEnabled(False)
        self.view.deleteMonumentBtn.setEnabled(False)
        self.monument_details = None
    
    @pyqtSlot(QListWidgetItem)
    def on_monument_click(self, item):
        """Обработка клика по элементу в списке."""
        monument_id = item.data(1)  # Получаем ID памятника
        self.monument_details = self.db_manager.get_monument_by_id(monument_id)

        # Показываем информацию о памятнике
        self.show_monument_details(self.monument_details)
        
    def update_buttons_state(self):
        """Активирует кнопки, если есть выбранный элемент."""
        is_selected = bool(self.view.monument_list_widget.selectedItems())
        self.view.readMonumentBtn.setEnabled(is_selected)
        self.view.createMonumentBtn.setEnabled(is_selected)
        self.view.updateMonumentBtn.setEnabled(is_selected)
        self.view.deleteMonumentBtn.setEnabled(is_selected)

    def show_monument_details(self, details):
        """Отображаем информацию о памятнике."""
        # Реализуйте отображение данных в нужном окне или компоненте
        print(details)