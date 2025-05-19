import os
from PyQt5.QtWidgets import QWidget, QDialog
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtCore import QObject, pyqtSlot, Qt
from PyQt5.uic import loadUi
import config
from views.monumets_list_window.read_monument import ReadMonumentController
from views.monumets_list_window.delete_monument import DeleteMonumentController
from views.monumets_list_window.update_monument import UpdateMonumentController
from views.monumets_list_window.create_monument import CreateMonumentController
from utils.base_classes import BaseView



class MonumentListView(QWidget, BaseView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_ui("monuments_list_window.ui")

        # Настройка модели таблицы
        self.model = QSqlTableModel(self)
        self.model.setTable("Monuments")
        self.model.select()
        self.model.setHeaderData(0, Qt.Horizontal, "ID")
        self.model.setHeaderData(1, Qt.Horizontal, "Название")

        self.monumentsTableView.setModel(self.model)
        self.monumentsTableView.resizeColumnsToContents()
        self.monumentsTableView.setSortingEnabled(True)


class MonumentListController(QObject):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.view = MonumentListView()
        self.current_monument_id = None

        self.setup_connections()
        self.update_buttons_state(False)

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
            monument = self.db_manager.get_monument_by_id(self.current_monument_id)
            self.read_monument = ReadMonumentController(monument_data=monument)
            self.read_monument.show()

    @pyqtSlot()
    def create_monument(self):
        self.create_monument = CreateMonumentController(db_manager=self.db_manager)
        result = self.create_monument.view.exec()
        if result == QDialog.Accepted:
            self.refresh_data()  # Обновляем после успешного создания

    @pyqtSlot()
    def update_monument(self):
        if self.current_monument_id:
            monument = self.db_manager.get_monument_by_id(self.current_monument_id)
            self.update_monument = UpdateMonumentController(monument_details=monument, db_manager=self.db_manager)
            result = self.update_monument.view.exec()
            if result == QDialog.Accepted:
                self.refresh_data()

    @pyqtSlot()
    def delete_monument(self):
        if self.current_monument_id:
            monument = self.db_manager.get_monument_by_id(self.current_monument_id)
            self.delete_dialog = DeleteMonumentController(monument_details=monument, db_manager=self.db_manager)
            result = self.delete_dialog.view.exec()
            if result == QDialog.Accepted:
                self.refresh_data()

    @pyqtSlot()
    def refresh_data(self):
        self.view.model.select()
        self.update_buttons_state(False)
        self.current_monument_id = None
