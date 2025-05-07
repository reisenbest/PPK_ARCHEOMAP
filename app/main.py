# main.py

import sys
from PyQt5.QtWidgets import QApplication
from views.main_menu import MainMenuView  

if __name__ == "__main__":
    app = QApplication(sys.argv)  # Создаём экземпляр приложения
    window = MainMenuView()  # Создаём окно из main_window.py
    window.show()  # Показываем окно
    sys.exit(app.exec_())  # Запускаем цикл обработки событий