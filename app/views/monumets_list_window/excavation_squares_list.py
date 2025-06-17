import os
import sys
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QObject
from PyQt5.uic import loadUi
from utils.base_classes import BaseView
from app.views.monumets_list_window.excavation_squares_manage import PutExcavationSquaresController
import config
import json
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QAbstractItemView


class ExcavationSquaresListView(QDialog, BaseView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_ui('excavation_squares_list_dialog.ui')  # путь должен быть правильный
        


class ExcavationSquaresListController(QObject):
    def __init__(self, monument_id, db_manager, parent=None):
        super().__init__(parent)
        
        self.monument_id = monument_id
        self.db_manager = db_manager

        self.view = ExcavationSquaresListView()
        self.setup_connections()
        self.load_excavation_squares(monument_id=self.monument_id)
        self.excavation_squares_create_window = PutExcavationSquaresController(parent=self.view, monument_id=monument_id,
                                                                            db_manager=self.db_manager)


        self.excavation_squares_create_window.square_saved.connect(self.on_square_saved)


    def setup_connections(self):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
        self.view.addPolygonBtn.clicked.connect(self.put_polygon)
        self.view.deletePolygonBtn.clicked.connect(self.delete_polygon)
        self.view.updatePolygonBtn.clicked.connect(self.update_polygon)

        # Настройка поведения при выделении строк
        self.view.polygonsTableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.view.polygonsTableView.setSelectionMode(QAbstractItemView.SingleSelection)

        self.view.deletePolygonBtn.setEnabled(False)  # отключаем кнопку по умолчанию
        self.view.updatePolygonBtn.setEnabled(False)  # отключаем кнопку по умолчанию

        
    def show(self):
        self.view.show()

    def put_polygon(self):
        self.excavation_squares_create_window.show()  


    def delete_polygon(self):
        row = self.view.polygonsTableView.selectionModel().selectedRows()[0].row()
        square_id = self.model.data(self.model.index(row, 0))

        confirm = QMessageBox.question(
            self.view,
            "Подтвердите удаление",
            f"Вы уверены, что хотите удалить полигон с ID {square_id}?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            try:
                self.db_manager.excavation_squares_table.delete_excavation_square_by_own_id(int(square_id))
                self.load_excavation_squares(self.monument_id)
            except Exception as e:
                QMessageBox.critical(self.view, "Ошибка удаления views lvl", str(e))

    def update_polygon(self):
        indexes = self.view.polygonsTableView.selectionModel().selectedRows()
        if not indexes:
            return

        row = indexes[0].row()
        square_id = int(self.model.item(row, 0).text())
        geometry = self.model.item(row, 1).text()
        description = self.model.item(row, 2).text()

        # Парсим GeoJSON
        # try:
        #     geojson = json.loads(geometry)
        #     coordinates = geojson["coordinates"][0]  # предполагается Polygon
        # except Exception as e:
        #     QMessageBox.critical(self.view, "Ошибка", f"Некорректная геометрия: {e}")
        #     return

        existing_data = {
            "square_id": square_id,
            "geom_description": description,
            "geometry": geometry
        }

        
        excavation_squares_update_window = PutExcavationSquaresController(
            monument_id=self.monument_id,
            db_manager=self.db_manager,
            existing_data=existing_data,
            parent=self.view
        )

        excavation_squares_update_window.square_saved.connect(self.on_square_saved)
        excavation_squares_update_window.show()

    def load_excavation_squares(self, monument_id):
        
        try:
            excavation_squares = self.db_manager.excavation_squares_table.get_excavation_squares_list_by_monument_id(monument_id)
        except Exception as e:
            QMessageBox.critical(self.view, "Ошибка загрузки", str(e))
            return

        model = QStandardItemModel(len(excavation_squares), 3)
        model.setHorizontalHeaderLabels(["square_id", "geometry", "geom_description"])

        for row_idx, square in enumerate(excavation_squares):
            model.setItem(row_idx, 0, QStandardItem(str(square["square_id"])))
            model.setItem(row_idx, 1, QStandardItem(square["geometry"]))
            model.setItem(row_idx, 2, QStandardItem(square.get("geom_description", "")))

        self.view.polygonsTableView.setModel(model)
        self.view.polygonsTableView.resizeColumnsToContents()
        self.model = model

        # Безопасное переподключение
        selection_model = self.view.polygonsTableView.selectionModel()
        if selection_model:
            try:
                selection_model.selectionChanged.disconnect(self.on_selection_changed)
            except TypeError:
                pass
            selection_model.selectionChanged.connect(self.on_selection_changed)

    def on_square_saved(self):
        self.load_excavation_squares(self.monument_id)

    def on_selection_changed(self):
        selected = self.view.polygonsTableView.selectionModel().hasSelection()
        self.view.deletePolygonBtn.setEnabled(selected)
        self.view.updatePolygonBtn.setEnabled(selected)  # новая строка




