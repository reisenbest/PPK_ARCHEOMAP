from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMessageBox
import os
import config

class BaseView:
    def load_ui(self, ui_filename):
        try:
            ui_path = os.path.join(config.UI_DIR, ui_filename)
            loadUi(ui_path, self)
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Ошибка загрузки интерфейса",
                f"Не удалось загрузить UI файл '{ui_filename}':\n\n{str(e)}"
            )

# class BaseController:
#     def __init__(self, view_class, db_manager=None, parent=None):
#         super().__init__(parent)
#         self.view = view_class()
#         self.db_manager = db_manager

#         try:
#             self.setup_connections()
#         except Exception as e:
#             self.show_error(f"Ошибка при настройке подключений:\n{e}")
