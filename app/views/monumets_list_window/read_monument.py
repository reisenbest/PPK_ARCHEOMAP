
import os
import sys
import config
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot, QObject
from PyQt5.uic import loadUi



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

class ReadMonumentView(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        ui_path = os.path.join(config.UI_DIR, 'read_monument_window.ui')
        loadUi(ui_path, self)

    def display_monument_details(self, details):
        print('Детали памятника:', details)

        content = f"""
            <h2>{details['monument_id']}</h2>
            <h2>Описание</h2>
            <p>{details['name']}</o>
            <h2>Описание</h2>
            <p>{details['description']}</p>
            <h2>Объект</h2>
            <p>{details['research_object']}</p>
        """
        self.MonumentContainer.setHtml(content)

class ReadMonumentController(QObject):
    def __init__(self,  monument_details, parent=None):
        super().__init__(parent)
        self.view = ReadMonumentView()
        self.view.display_monument_details(monument_details)  # Заполняем окно данными
        self.setup_connections()

    def show(self):
        self.view.show()

    def setup_connections(self):
        pass