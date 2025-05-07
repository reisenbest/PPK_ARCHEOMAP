
from views.information_window.information_view import InformationView
from views.information_window.about_authors_view import AboutAuthorsView

class InformationController:
    def __init__(self):
        self.view = InformationView()
        self.setup_connections()

    def setup_connections(self):
        self.view.AboutAuthorsButton.clicked.connect(self.show_about_authors)

    def show(self):
        self.view.show()

    def show_about_authors(self):
        self.dialog = AboutAuthorsView()
        self.dialog.exec_()  # модальное окно