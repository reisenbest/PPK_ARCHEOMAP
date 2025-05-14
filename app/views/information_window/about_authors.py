
import os
import sys
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
import config

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

class AboutAuthorsView(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        ui_path = os.path.join(config.UI_DIR, 'about_authors_window.ui')
        loadUi(ui_path, self)