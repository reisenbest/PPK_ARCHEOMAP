import os
import sys
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QObject
from PyQt5.uic import loadUi
from utils.base_classes import BaseView
from app.views.monumets_list_window.excavation_squares_manage import PutExcavationSquaresController
import config
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem

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
        self.excavation_squares_list_window = PutExcavationSquaresController(parent=self.view, monument_id=monument_id,
                                                                            db_manager=self.db_manager)


        self.excavation_squares_list_window.square_saved.connect(self.on_square_saved)


    def setup_connections(self):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
        self.view.addPolygonBtn.clicked.connect(self.put_polygon)
        self.view.deletePolygonBtn.clicked.connect(self.deletePolygonBtn)
                                                      
        
    def show(self):
        self.view.show()

    def put_polygon(self, arg):
      self.excavation_squares_list_window.show()  
      print(self.monument_id)

    def deletePolygonBtn(self, arg):
      pass

    def load_excavation_squares(self, monument_id):
        try:
            excavation_squares = self.db_manager.excavation_squares_table.get_excavation_squares_list_by_monument_id(monument_id)
        except Exception as e:
            QMessageBox.critical(self.view, "Ошибка загрузки", str(e))
            return
        
        print('АТТЕНЩШЕН', excavation_squares)

        model = QStandardItemModel(len(excavation_squares), 3)
        model.setHorizontalHeaderLabels(["square_id", "geometry", "geom_description"])

        for row_idx, excavation_square_obj in enumerate(excavation_squares):
            print(excavation_square_obj)
            model.setItem(row_idx, 0, QStandardItem(str(excavation_square_obj["square_id"])))
            model.setItem(row_idx, 1, QStandardItem(excavation_square_obj["geometry"]))
            model.setItem(row_idx, 2, QStandardItem(excavation_square_obj.get("geom_description", "")))


        self.view.polygonsTableView.setModel(model)
        self.view.polygonsTableView.resizeColumnsToContents()
        self.model = model  # сохраним модель, если потом нужно удаление

    def on_square_saved(self):
        self.load_excavation_squares(self.monument_id)




