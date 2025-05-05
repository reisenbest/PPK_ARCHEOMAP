from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import sys
import os

class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ArcheoMap")
        self.setGeometry(100, 100, 1200, 800)

        # Веб-виджет
        self.browser = QWebEngineView()

        # Правильно формируем путь
        path = os.path.abspath("./OSM/index.html")
        url = QUrl.fromLocalFile(path)

        self.browser.load(url)
        self.setCentralWidget(self.browser)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MapWindow()
    window.show()
    sys.exit(app.exec_())
