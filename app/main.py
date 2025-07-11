import sys
import os
from PyQt5.QtWidgets import QApplication
from views.main_menu_window.main_menu import MainMenuController
from database.db_main_connection import UnionDataBaseManagerController

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):  # type: ignore
        # Запущено из exe, ресурсы во временной папке
        return os.path.join(sys._MEIPASS, relative_path)
    # Запущено из исходников
    return os.path.join(os.path.abspath("."), relative_path)


def main():
    app = QApplication(sys.argv)
    app.setStyle('Windows')

    # Инициализируем менеджер БД на основе QSql
    db_manager = UnionDataBaseManagerController()

    # Передаём менеджер контроллеру
    controller = MainMenuController(db_manager=db_manager)
    controller.show()

    exit_code = app.exec_()

    # Закрываем соединение при завершении
    db_manager.db_common.close()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
