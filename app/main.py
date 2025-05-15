import sys
from PyQt5.QtWidgets import QApplication
from views.main_menu_window.main_menu import MainMenuController
from database.db_main_connection import DataBaseManager

def main():
    app = QApplication(sys.argv)

    # Инициализируем менеджер БД на основе QSql
    db_manager = DataBaseManager()

    # Передаём менеджер контроллеру
    controller = MainMenuController(db_manager=db_manager)
    controller.show()

    exit_code = app.exec_()

    # Закрываем соединение при завершении
    db_manager.close()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()