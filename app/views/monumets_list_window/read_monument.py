
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

      name, description, date, location = details
      content = f"""
        <h1>{name}</h1>
        <h2>Описание</h2>
        <p>{description}</p>
        <h2>Дата</h2>
        <p>{date}</p>
        <h2>Местоположение</h2>
        <p>{location}</p>
    """
      self.MonumentContainer.setHtml(content)

class ReadMonumentController(QObject):
    def __init__(self, monument_details, parent=None):
        super().__init__(parent)
        self.view = ReadMonumentView()
        self.view.display_monument_details(monument_details)  # Заполняем окно данными
        self.setup_connections()

    def show(self):
        self.view.show()

    def setup_connections(self):
        pass