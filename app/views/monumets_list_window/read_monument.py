import os
from PyQt5.QtWidgets import QDialog, QMenu, QFileDialog
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from utils.base_classes import BaseView
from utils.utils import UtilsForViews
import config
import subprocess


class ReadMonumentView(QDialog, BaseView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_ui('read_monument_window.ui')
        self.utils = UtilsForViews()

        # Отключаем автоматическое открытие ссылок в QTextBrowser
        self.MonumentContainer.setOpenLinks(False)

        # Подключаем обработчик клика по ссылкам
        self.MonumentContainer.anchorClicked.connect(self.open_file_from_link)
        self.MonumentContainer.installEventFilter(
            self)  # Для перехвата событий мыши

    def eventFilter(self, obj, event):
        if obj == self.MonumentContainer and event.type() == event.MouseButtonPress:
            if event.button() == 2:  # Правая кнопка мыши
                cursor = self.MonumentContainer.cursorForPosition(event.pos())
                anchor = cursor.block().text()
                url = self.MonumentContainer.anchorAt(event.pos())
                if url:
                    menu = QMenu(self)
                    open_with = menu.addAction("Открыть с помощью...")
                    action = menu.exec_(
                        self.MonumentContainer.mapToGlobal(event.pos()))
                    if action == open_with:
                        app_path, _ = QFileDialog.getOpenFileName(
                            self, "Выберите приложение")
                        if app_path:
                            file_path = QUrl.fromPercentEncoding(url.encode())
                            if file_path.startswith("file://"):
                                file_path = file_path[7:]
                            absolute_path = os.path.abspath(
                                os.path.join(config.DATA_STORAGE_DIR, file_path))
                            subprocess.Popen([app_path, absolute_path])
                    return True
        return super().eventFilter(obj, event)

    def display_monument_data(self, data):
        print('Детали памятника:', data)

        content = self.utils.read_monument_content(data)

        self.MonumentContainer.setHtml(content)

    def open_file_from_link(self, url: QUrl):
        # Декодируем URL
        file_path = QUrl.fromPercentEncoding(url.toString().encode())

        # Убираем схему "file://", если есть
        if file_path.startswith("file://"):
            file_path = file_path[7:]

        # Строим абсолютный путь к файлу, относительно config.DATA_STORAGE_DIR
        absolute_path = os.path.abspath(
            os.path.join(config.DATA_STORAGE_DIR, file_path))

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
