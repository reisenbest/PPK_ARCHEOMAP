import os
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from utils.base_classes import BaseView
import config


class ReadMonumentView(QDialog, BaseView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_ui('read_monument_window.ui')
        
        # Отключаем автоматическое открытие ссылок в QTextBrowser
        self.MonumentContainer.setOpenLinks(False)
        
        # Подключаем обработчик клика по ссылкам
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
                        <b>Тип файла: {file['file_type']}</b>: описание: {file['file_description']}<br>
                        <i><a href="{file['file_path']}">{file['file_path']}</a></i>
                    </li>
                """
            content += "</ul>"
        else:
            content += "<h2>Файлы</h2><p>Нет прикреплённых файлов.</p>"

        self.MonumentContainer.setHtml(content)

    def open_file_from_link(self, url: QUrl):
        # Декодируем URL
        file_path = QUrl.fromPercentEncoding(url.toString().encode())

        # Убираем схему "file://", если есть
        if file_path.startswith("file://"):
            file_path = file_path[7:]

        # Строим абсолютный путь к файлу, относительно config.DATA_STORAGE_DIR
        absolute_path = os.path.abspath(os.path.join(config.DATA_STORAGE_DIR, file_path))

        print(f"Ищем файл по пути: {absolute_path}")

        if os.path.exists(absolute_path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(absolute_path))
        else:
            print(f"Файл не найден: {absolute_path}")


class ReadMonumentController:
    def __init__(self, monument_data, parent=None):
        self.view = ReadMonumentView(parent)
        self.view.display_monument_data(monument_data)

    def show(self):
        self.view.show()
