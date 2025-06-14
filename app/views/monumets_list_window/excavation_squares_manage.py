
import os
import sys
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QObject
from PyQt5.uic import loadUi
from utils.base_classes import BaseView
import config
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

class PutExcavationSquaresView(QDialog, BaseView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.load_ui('excavation_squares_manage_window.ui')
        self.setWindowModality(Qt.ApplicationModal)  # Блокирует все окна приложения
        


class PutExcavationSquaresController(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.view = PutExcavationSquaresView(parent)  # ← передай родителя
        self.setup_connections()

        self.view.updatePointBtn.setEnabled(False)
        self.view.removePointBtn.setEnabled(False)
        self.view.moveUpBtn.setEnabled(False)
        self.view.moveDownBtn.setEnabled(False)

    def setup_connections(self):
        self.view.cancelBtn.clicked.connect(self.cancel_button)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
        self.view.saveBtn.clicked.connect(self.save_button)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
        self.view.addPointBtn.clicked.connect(self.add_point_button)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
        self.view.removePointBtn.clicked.connect(self.remove_point_button)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
        self.view.moveUpBtn.clicked.connect(self.move_up_point_button)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
        self.view.moveDownBtn.clicked.connect(self.move_down_point_button)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
        self.view.updatePointBtn.clicked.connect(self.update_point_button)
        self.view.pointsList.itemSelectionChanged.connect(self.update_buttons_state)


        # Настройка колонок таблицы
        self.view.pointsList.setColumnCount(2)
        self.view.pointsList.setHorizontalHeaderLabels(['Latitude', 'Longitude'])                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         


        
    def show(self):
        self.clear_view_data()
        self.view.show()



    def add_point_button(self, arg):
        lat = self.view.latSpinBox.value()
        lon = self.view.lonSpinBox.value()

        row = self.view.pointsList.rowCount()
        self.view.pointsList.insertRow(row)

        self.view.pointsList.setItem(row, 0, QTableWidgetItem(f"{lat:.6f}"))
        self.view.pointsList.setItem(row, 1, QTableWidgetItem(f"{lon:.6f}"))


    def remove_point_button(self, arg):
        self.view.reject()

    def move_up_point_button(self, arg):
        self.view.reject()

    def move_down_point_button(self, arg):
        self.view.reject()

    def update_point_button(self, arg):
        self.view.reject()

    def cancel_button(self, arg):
        self.view.reject()

    def save_button(self, arg):
        self.view.reject()

    def update_buttons_state(self):
        selected = self.view.pointsList.selectedItems()
        has_selection = bool(selected)

        self.view.updatePointBtn.setEnabled(has_selection)
        self.view.removePointBtn.setEnabled(has_selection)
        self.view.moveUpBtn.setEnabled(has_selection)
        self.view.moveDownBtn.setEnabled(has_selection)
    
    def clear_view_data(self):
        self.view.latSpinBox.setValue(0.0)
        self.view.lonSpinBox.setValue(0.0)
        self.view.descriptionEdit.clear()
        self.view.pointsList.setRowCount(0)  # Очищает все строки таблицы
        self.update_buttons_state()