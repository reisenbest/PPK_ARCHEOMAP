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
    def copy_selected_files_to_monument_folder(self,  view_obj, selected_files: list, monument_path: str,) -> list:
        '''
        при создании памятника получает данные о выбранном файле 
        и копирует этот файл в директорию (папку) созданную для памятника
        СЕЙЧАС СДЕЛАНО ЦИКЛОМ НА БУДУЩЕЕ ЧТОБЫ МОЖНО БЫЛО ПРИ СОЗДАНИИ 
        ОБЪЕКТА МОНУМЕНТ ВЫБИРАТЬ СРАЗУ НЕСКОЛЬКО ФАЙЛОВ 
        НО ПОКА МОЖНО ВЫБИРАТЬ ТОЛЬКО ОДИН
        '''
        files_data = []

        for file_entry in selected_files:
            file_path = file_entry['path']
            description = file_entry['description']

            if os.path.exists(file_path):
                try:
                    filename = os.path.basename(file_path)
                    target_path = os.path.join(monument_path, filename)
                    shutil.copy(file_path, target_path)

                    relative_path = os.path.relpath(target_path, config.DATA_STORAGE_DIR)

                    files_data.append({
                        'file_path': relative_path,
                        'file_type': file_entry['file_type'],
                        'file_description': description
                    })
                except Exception as copy_err:
                    QMessageBox.warning(self.view, "Ошибка при копировании файла", f"{file_path}\n{str(copy_err)}")
                    return None  # или return []
            else:
                QMessageBox.warning(self.view, "Файл не найден", f"Файл не существует: {file_path}")
                return None

        return files_data

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
            
    def rename_monument_folder(self, old_path, new_path):
        '''
        изменение имени созданной папки при изменени имени монумента
        '''
        try:
            if os.path.exists(old_path):
                os.rename(old_path, new_path)
                print(
                    f"Папка переименована: {old_path} → {new_path}")
            elif not os.path.exists(new_path):
                os.makedirs(new_path)
                print(f"Создана новая папка памятника: {new_path}")
            return True
        except Exception as folder_err:
            QMessageBox.warning(
                self.view, "Ошибка переименования папки", str(folder_err))
            return False
    
    def rename_files_paths(self):
        '''
        изменение путей к файлам в БД при изменении папки
        '''
        pass
        
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


    def read_monument_content(self, data):
        '''
        возвращает html разметку для отображения контента. мб надо возвращать файл со стилями?? 
        пока так
        '''
        
        content = f"""
            <h2>ID памятника</h2>
            <p>{data['monument_id']}</p>

            <h2>Название</h2>
            <p>{data['name']}</p>

            <h2>Описание</h2>
            <p>{data['description']}</p>

            <h2>Объект исследования</h2>
            <p>{data['research_object']}</p>

            <h2>Широта</h2>
            <p>{data['latitude']}</p>

            <h2>Долгота</h2>
            <p>{data['longitude']}</p>

            <h2>Записка о координатах</h2>
            <p>{data['note']}</p>
        """

        files = data.get("files", [])
        if files:
            content += "<h2>Файлы</h2><ul>"
            for file in files:
                content += f"""
                    <li>
                        <b>Тип файла: {file['file_type']}</b>: описание: {file['file_description']}<br>
                        <i><a href="{file['file_path']}">{file['file_path']}</a></i>
                    </li>
                """
            content += "</ul>"
        else:
            content += "<h2>Файлы</h2><p>Нет прикреплённых файлов.</p>"

        excavation_squares = data.get("excavation_squares", [])
        if excavation_squares:
            content += "<h2>Территория исследования - поворотные точки</h2><ul>"
            for excavation_square in excavation_squares:
                content += f"""
                    <li>
                        <b>координаты: {excavation_square['geometry']}</b>: описание: {excavation_square['geom_description']}<br>
                    </li>
                """
            content += "</ul>"
        else:
            content += "<h2>Файлы</h2><p>Нет поворотные точки</p>"

        return content
