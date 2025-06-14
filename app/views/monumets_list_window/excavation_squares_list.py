import os
import sys
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QObject
from PyQt5.uic import loadUi
from utils.base_classes import BaseView
from app.views.monumets_list_window.excavation_squares_manage import PutExcavationSquaresController
import config


class ExcavationSquaresListView(QDialog, BaseView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_ui('excavation_squares_list_dialog.ui')  # путь должен быть правильный



class ExcavationSquaresListController(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.view = ExcavationSquaresListView()
        self.put_excavation_squares_window = PutExcavationSquaresController(self.view)
        self.setup_connections()


    def setup_connections(self):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
        self.view.addPolygonBtn.clicked.connect(self.put_polygon)
        self.view.deletePolygonBtn.clicked.connect(self.deletePolygonBtn)
                                                      
        
    def show(self):
        self.view.show()

    def put_polygon(self, arg):
      self.put_excavation_squares_window.show()  

    def deletePolygonBtn(self, arg):
      pass