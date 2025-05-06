import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import ui_test  # это сгенерированный файл из test.ui

class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # создаём экземпляр интерфейса
        self.ui = ui_test.Ui_MainWindow()
        self.ui.setupUi(self)  # инициализируем интерфейс внутри self

        # Загружаем локальную HTML-страницу в QWebEngineView
        path = os.path.abspath("./OSM/index.html")
        url = QUrl.fromLocalFile(path)
        self.ui.map.load(url)

        # Подключаем кнопку к выходу из приложения
        self.ui.pushButton.clicked.connect(QApplication.instance().quit)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MapWindow()
    window.show()
    sys.exit(app.exec_())