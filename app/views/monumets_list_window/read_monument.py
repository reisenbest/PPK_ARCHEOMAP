
import os
import sys
import config
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot, QObject
from PyQt5.uic import loadUi
from utils.base_classes import BaseView
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))




class ReadMonumentView(QDialog, BaseView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_ui('read_monument_window.ui')
        self.MonumentContainer.anchorClicked.connect(self.open_file_from_link)

    def display_monument_data(self, data):
        print('Детали памятника:', data)

        content = f"""
            <h2>ID памятника</h2>
            <p>{data['monument_id']}</p>

            <h2>Название</h2>
            <p>{data['name']}</p>

            <h2>Описание</h2>
            <p>{data['description']}</p>

            <h2>Объект исследования</h2>
            <p>{data['research_object']}</p>

            <h2>Широта</h2>
            <p>{data['latitude']}</p>

            <h2>Долгота</h2>
            <p>{data['longitude']}</p>

            <h2>Записка о координатах</h2>
            <p>{data['note']}</p>
        """

        files = data.get("files", [])
        if files:
            content += "<h2>Файлы</h2><ul>"
            for file in files:
                content += f"""
                    <li>
                        <b>{file['file_type']}</b>: {file['file_description']}<br>
                        <i><a href="{file['file_path']}">{file['file_path']}</a></i>
                    </li>
                """
            content += "</ul>"
        else:
            content += "<h2>Файлы</h2><p>Нет прикреплённых файлов.</p>"

        self.MonumentContainer.setHtml(content)

    def open_file_from_link(self, url: QUrl):
        # Decode the URL path to handle %-encoded characters
        file_path = QUrl.fromPercentEncoding(url.toString().encode())
        
        # Remove any URL scheme (like "file://") if present
        if file_path.startswith("file://"):
            file_path = file_path[7:]
        
        # Convert to absolute path
        absolute_path = os.path.abspath(os.path.join(config.BASE_APP_DIR, file_path))
        
        print(f"Ищем файл по пути: {absolute_path}")
        
        if os.path.exists(absolute_path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(absolute_path))
        else:
            print(f"Файл не найден: {absolute_path}")

class ReadMonumentController(QObject):
    def __init__(self,  monument_data, parent=None):
        super().__init__(parent)
        self.view = ReadMonumentView()
        self.view.display_monument_data(monument_data)  # Заполняем окно данными
        self.setup_connections()

    def show(self):
        self.view.show()

    def setup_connections(self):
        pass