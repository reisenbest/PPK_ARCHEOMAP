import sys
from PyQt5.QtWidgets import QApplication
from views.main_menu_window.main_menu_view import MainMenuView

from views.information_window.information_view import InformationView
from views.information_window.information_controller import InformationController

class MainMenuController:
    def __init__(self):
        self.view = MainMenuView()
        self.setup_connections()

    def setup_connections(self):
        self.view.MenuExitButton.clicked.connect(self.exit_app)
        self.view.MenuInfoButton.clicked.connect(self.open_information_window)

    def show(self):
        self.view.show()

    def exit_app(self):
        QApplication.quit()

    def open_information_window(self):
        self.info_controller = InformationController()
        self.info_controller.show()