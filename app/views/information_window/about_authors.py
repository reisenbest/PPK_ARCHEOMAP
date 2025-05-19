
import os
import sys
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QObject
from PyQt5.uic import loadUi
from utils.base_classes import BaseView
import config



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

class AboutAuthorsView(QDialog, BaseView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_ui('about_authors_windowc.ui')


class AboutAuthorsController(QObject):
    """docstring for AboutAuthorsController."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.view = AboutAuthorsView()

    def setup_connections(self):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
        pass

        
    def show(self):
        self.view.show()

    