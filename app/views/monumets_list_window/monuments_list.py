from PyQt5.QtSql import QSqlQueryModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem


from PyQt5.QtWidgets import QWidget, QDialog, QLineEdit
from PyQt5.QtSql import QSqlTableModel, QSqlQueryModel
from PyQt5.QtCore import QObject, pyqtSlot, Qt
from PyQt5.uic import loadUi
import config
from views.monumets_list_window.read_monument import ReadMonumentController
from views.monumets_list_window.delete_monument import DeleteMonumentController
from views.monumets_list_window.update_monument import UpdateMonumentController
from views.monumets_list_window.create_monument import CreateMonumentController
from utils.base_classes import BaseView
from utils.utils import UtilsForViews
from PyQt5.QtSql import QSqlQuery
from database.db_queries import DataBaseQueriesManager


class MonumentListView(QWidget, BaseView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_ui("monuments_list_window.ui")
        self.db_query_manager = DataBaseQueriesManager()

        # Используем QSqlQueryModel для JOIN-запроса
        self.model = QSqlQueryModel(self)
        self.model.setQuery(
            self.db_query_manager.monuments_table.create_monuments_list_view_query())

        self.monumentsTableView.setModel(self.model)
        self.monumentsTableView.resizeColumnsToContents()
        self.monumentsTableView.setSortingEnabled(True)

        self.searchLineEdit = self.findChild(QLineEdit, "searchLineEdit")


class MonumentListController(QObject):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.view = MonumentListView()
        self.utils = UtilsForViews(self.view)
        self.current_monument_id = None

        self.db_query_manager = DataBaseQueriesManager()

        self.setup_connections()
        self.update_buttons_state(False)

        self.view.searchLineEdit.textChanged.connect(
            self.on_search_text_changed)

    def show(self):
        self.view.show()

    def setup_connections(self):
        selection_model = self.view.monumentsTableView.selectionModel()
        selection_model.selectionChanged.connect(self.on_selection_changed)

        self.view.readMonumentBtn.clicked.connect(self.show_read_monument)
        self.view.createMonumentBtn.clicked.connect(self.create_monument)
        self.view.updateMonumentBtn.clicked.connect(self.update_monument)
        self.view.deleteMonumentBtn.clicked.connect(self.delete_monument)
        self.view.refreshBtn.clicked.connect(self.refresh_data)

    def get_selected_monument_id(self):
        indexes = self.view.monumentsTableView.selectionModel().selectedRows()
        if indexes:
            row = indexes[0].row()
            return self.view.model.data(self.view.model.index(row, 0))
        return None

    @pyqtSlot()
    def on_selection_changed(self):
        self.current_monument_id = self.get_selected_monument_id()
        self.update_buttons_state(bool(self.current_monument_id))

    def update_buttons_state(self, enabled: bool):
        self.view.readMonumentBtn.setEnabled(enabled)
        self.view.updateMonumentBtn.setEnabled(enabled)
        self.view.deleteMonumentBtn.setEnabled(enabled)
        self.view.createMonumentBtn.setEnabled(True)

    @pyqtSlot()
    def show_read_monument(self):
        if self.current_monument_id:
            monument = self.db_manager.monuments_table.get_monument_by_id(
                self.current_monument_id)
            self.read_monument = ReadMonumentController(monument_data=monument)
            self.read_monument.show()

    @pyqtSlot()
    def create_monument(self):
        create_controller = CreateMonumentController(
            db_manager=self.db_manager)
        self.utils.execute_operation_on_menu_buttons(controller_instance=create_controller,
                                                     refresh_data_method=self.refresh_data)

    @pyqtSlot()
    def update_monument(self):
        if self.current_monument_id:
            monument = self.db_manager.monuments_table.get_monument_by_id(
                self.current_monument_id)
            update_controller = UpdateMonumentController(
                monument_details=monument, db_manager=self.db_manager)
            self.utils.execute_operation_on_menu_buttons(controller_instance=update_controller,
                                                         refresh_data_method=self.refresh_data)

    @pyqtSlot()
    def delete_monument(self):
        if self.current_monument_id:
            monument = self.db_manager.monuments_table.get_monument_by_id(
                self.current_monument_id)
            self.delete_dialog = DeleteMonumentController(
                monument_details=monument, db_manager=self.db_manager)

            self.utils.execute_operation_on_menu_buttons(controller_instance=self.delete_dialog,
                                                         refresh_data_method=self.refresh_data)

    @pyqtSlot()
    def refresh_data(self):
        query_text = self.db_manager.db_queries.monuments_table.get_monuments_query()
        self.view.model.setQuery(query_text, self.db_manager.db_common.db)
        self.update_buttons_state(False)
        self.current_monument_id = None

    def on_search_text_changed(self, text):
        # Преобразуем введённый пользователем текст поиска к нижнему регистру для нечувствительного поиска
        lower_text = text.lower()
        
        # Получаем количество строк и столбцов в текущей модели данных таблицы
        rows = self.view.model.rowCount()
        cols = self.view.model.columnCount()
        
        # Получаем заголовки столбцов из модели для последующего отображения в новой модели
        # Важно: Qt.Horizontal указывает, что мы берём заголовки по горизонтали (столбцы)
        headers = [self.view.model.headerData(i, 1) for i in range(cols)]  # 1 == Qt.Horizontal
        
        filtered = []  # Список для хранения строк, которые подходят под критерий поиска
        
        # Проходим по всем строкам модели
        for row in range(rows):
            row_data = []  # Список для хранения значений текущей строки
            match = False  # Флаг, указывающий, есть ли совпадение по поиску в этой строке
            
            # Проходим по всем столбцам строки
            for col in range(cols):
                # Получаем значение ячейки, преобразуем к строке (на случай None)
                value = str(self.view.model.data(self.view.model.index(row, col)) or "")
                row_data.append(value)  # Добавляем значение в список текущей строки
                
                # Проверяем, содержится ли поисковый текст в значении ячейки (без учёта регистра)
                if lower_text in value.lower():
                    match = True  # Если совпадение найдено, отмечаем это
            
            # Если хотя бы в одной ячейке строки найдено совпадение, добавляем всю строку в результат
            if match:
                filtered.append(row_data)
        
        # Создаём новую модель для отображения отфильтрованных данных
        model = QStandardItemModel()
        
        # Устанавливаем заголовки столбцов в новую модель
        model.setHorizontalHeaderLabels(headers)
        
        # Добавляем отфильтрованные строки в новую модель
        for row_data in filtered:
            # Преобразуем каждое значение строки в QStandardItem и добавляем строку в модель
            items = [QStandardItem(str(val)) for val in row_data]
            model.appendRow(items)
        
        # Устанавливаем новую модель в таблицу для отображения пользователю
        self.view.monumentsTableView.setModel(model)
