import sys
from PyQt5.QtWidgets import QApplication
from views.main_menu_window.main_menu import MainMenuController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = MainMenuController()
    controller.show()
    sys.exit(app.exec_())