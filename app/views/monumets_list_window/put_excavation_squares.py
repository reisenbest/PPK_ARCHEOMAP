
import os
import sys
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QObject
from PyQt5.uic import loadUi
from utils.base_classes import BaseView
import config



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

class PutExcavationSquaresView(QDialog, BaseView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_ui('put_excavation_squares_window.ui')


class PutExcavationSquaresController(QObject):
    """docstring for AboutAuthorsController."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.view = PutExcavationSquaresView()

    def setup_connections(self):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
        pass

        
    def show(self):
        self.view.show()