import sys
from PyQt5.QtWidgets import QApplication
from views.main_menu_window.main_menu import MainMenuController
from database.db_main_connection import DataBaseManager

def main():
    app = QApplication(sys.argv)

    # Создаём менеджер базы данных
    db_manager = DataBaseManager()

    # Создаём контроллер главного меню и передаём ему менеджер базы данных
    controller = MainMenuController(db_manager=db_manager)
    controller.show()

    exit_code = app.exec_()

    # Закрываем соединение с базой данных при выходе
    db_manager.close()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()