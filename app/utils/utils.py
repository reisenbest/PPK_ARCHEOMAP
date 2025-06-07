import os
from PyQt5.QtWidgets import QFileDialog, QInputDialog, QMessageBox
import config
import shutil
from PyQt5.QtWidgets import QWidget, QDialog

# class UtilsForViews(object):
#   """docstring for UtilsForViews."""
#   def __init__(self, arg):
#     super(UtilsForViews, self).__init__()
#   arg

  
class UtilsForViews:
    def __init__(self):
      pass

    def browse_file_in_file_system(self, view_obj):
        '''
        принмиает self view связанного с контроллером 
        реализация диалогового окна с выбором файла на компьютере
        используется для загурзки файлов при создании и имземеннии объекта в БД
        '''
        file_path, _ = QFileDialog.getOpenFileName(view_obj, "Выберите файл", "", "Все файлы (*.*)")
        if not file_path:
            return

        # Ввод описания файла
        description, ok = QInputDialog.getText(view_obj, "Описание файла", f"Введите описание для:\n{os.path.basename(file_path)}")
        if not ok:
            return

        # Ввод типа файла
        file_type, ok_type = QInputDialog.getText(view_obj, "Тип файла", f"Введите тип для:\n{os.path.basename(file_path)} (например: pdf, jpg, obj, txt...)")
        if not ok_type:
            return
        
        return {
        'path': file_path,
        'description': description.strip(),
        'file_type': file_type.strip()
    }



    def create_monument_folder(self, monument_path):
        '''
        создание папки для монумента при его создании
        все оперции с os и пр
        '''
        try:
          os.makedirs(monument_path, exist_ok=True)
        except Exception as folder_err:
          QMessageBox.warning(self.view, "Ошибка при создании папки", str(folder_err))
          return
    
    def delete_monument_folder(self, monument_name):
        '''
        удаление папки и ее содержимого для монумента при его удалении
        все оперции с os и пр
        '''
        try:
          monument_path = os.path.join(config.DATA_STORAGE_DIR, monument_name)
          if os.path.exists(monument_path):
                          shutil.rmtree(monument_path)
                          print(f"Папка памятника удалена: {monument_path}")
        except Exception as folder_err:
            QMessageBox.warning(
                        self.view,
                        "Предупреждение",
                        f"Памятник удалён из базы данных,\n"
                        f"но произошла ошибка при удалении папки:\n{folder_err}"
                        )
            
    
    def execute_operation_on_menu_buttons(self, controller_instance, refresh_data_method):
        '''
        удаление папки и ее содержимого для монумента при его удалении
        все оперции с os и пр.
        принимает экземпляр класса контроллера, с которым связана кнопка (и соотвественно метод)
        '''
        result = controller_instance.view.exec()
        #если закрыл окно через ОКЕЙ то выполняем обновление окна основного со списком памятников чтобы подтянуть произошедшие изменения
        if result == QDialog.Accepted: 
            refresh_data_method()  # Обновляем после успешного создания
