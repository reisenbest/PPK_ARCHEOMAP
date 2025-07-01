import os
from PyQt5.QtWidgets import QFileDialog, QInputDialog, QMessageBox
import config
import shutil
from PyQt5.QtWidgets import QWidget, QDialog
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtCore import Qt


class UtilsForViews:
    def __init__(self, view=None):
        self.view = view

    def browse_file_in_file_system(self):
        '''
        принмиает self view связанного с контроллером 
        реализация диалогового окна с выбором файла на компьютере
        используется для загурзки файлов при создании и имземеннии объекта в БД
        '''
        file_path, _ = QFileDialog.getOpenFileName(
            self.view, "Выберите файл", "", "Все файлы (*.*)")
        if not file_path:
            return

        # Ввод описания файла
        description, ok = QInputDialog.getText(
            self.view, "Описание файла", f"Введите описание для:\n{os.path.basename(file_path)}")
        if not ok:
            return

        # Ввод типа файла
        file_type, ok_type = QInputDialog.getText(
            self.view, "Тип файла", f"Введите тип для:\n{os.path.basename(file_path)} (например: pdf, jpg, obj, txt...)")
        if not ok_type:
            return

        return {
            'path': file_path,
            'description': description.strip(),
            'file_type': file_type.strip()
        }

    def copy_selected_files_to_monument_folder(self, selected_files: list, monument_path: str,):
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

                    relative_path = os.path.relpath(
                        target_path, config.DATA_STORAGE_DIR)

                    files_data.append({
                        'file_path': relative_path,
                        'file_type': file_entry['file_type'],
                        'file_description': description
                    })
                except Exception as copy_err:
                    QMessageBox.warning(
                        self.view, "Ошибка при копировании файла", f"{file_path}\n{str(copy_err)}")
                    return None  # или return []
            else:
                QMessageBox.warning(self.view, "Файл не найден",
                                    f"Файл не существует: {file_path}")
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
            QMessageBox.warning(
                self.view, "Ошибка при создании папки", str(folder_err))
            return

    def delete_monument_folder(self, monument_name):
        '''
        удаление папки и ее содержимого для монумента при его удалении
        все оперции с os и пр
        '''
        try:
            monument_path = os.path.join(
                config.DATA_STORAGE_DIR, monument_name)
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

    def execute_operation_on_menu_buttons(self, controller_instance, refresh_data_method):
        '''
        удаление папки и ее содержимого для монумента при его удалении
        все оперции с os и пр.
        принимает экземпляр класса контроллера, с которым связана кнопка (и соотвественно метод)
        '''
        result = controller_instance.view.exec()
        # если закрыл окно через ОКЕЙ то выполняем обновление окна основного со списком памятников чтобы подтянуть произошедшие изменения
        if result == QDialog.Accepted:
            refresh_data_method()  # Обновляем после успешного создания

    def read_monument_content(self, data):
        '''
        Возвращает HTML-разметку с встроенными стилями для отображения информации о памятнике.
        '''
        style = """
            <style>
                body {
                    font-family: Tahoma, Arial, sans-serif;
                    font-size: 13px;
                    color: #000;
                    background-color: #e0e0e0;
                    padding: 10px;
                }
                h2 {
                    font-size: 15px;
                    margin: 15px 0 5px 0;
                    color: #333;
                    border-bottom: 1px solid #999;
                    padding-bottom: 2px;
                }
                p {
                    margin: 5px 0 10px 0;
                }
                ul {
                    padding-left: 20px;
                }
                li {
                    margin-bottom: 8px;
                }
                a {
                    color: #003399;
                    text-decoration: none;
                }
                a:hover {
                    text-decoration: underline;
                }
                .section {
                    margin-bottom: 15px;
                    background: #f5f5f5;
                    padding: 10px;
                    border: 1px solid #bbb;
                    border-radius: 4px;
                }
            </style>
        """

        content = f"""
            {style}
            <div class="section">
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
            </div>
        """

        files = data.get("files", [])
        if files:
            content += """
                <div class="section">
                    <h2>Файлы</h2>
                    <ul style='list-style: none; padding-left: 0;'>
            """
            icon_map = {
                'pdf': '📄',
                'doc': '📄',
                'docx': '📄',
                'jpg': '🖼️',
                'jpeg': '🖼️',
                'png': '🖼️',
                'mp4': '🎞️',
                'avi': '🎞️',
                'mp3': '🎵',
                'wav': '🎵',
                'txt': '📄',
                'zip': '🗜️',
                'rar': '🗜️',
                'glb': '🧊',
                'default': '📁'
            }
            for file in files:
                ext = file['file_path'].split('.')[-1].lower()
                icon = icon_map.get(ext, icon_map['default'])
                content += f"""
                    <li style='margin-bottom: 12px; padding: 8px; background: #f0f0f0; border: 1px solid #bbb; border-radius: 4px;'>
                        <span style='font-size: 18px; margin-right: 8px;'>{icon}</span>
                        <b>{file['file_type']}</b><br>
                        <span style='color: #555;'>{file['file_description']}</span><br>
                        <a href=\"{file['file_path']}\" style='color: #003399; font-weight: bold; word-break: break-all;'>{file['file_path']}</a>
                    </li>
                """
            content += "</ul></div>"
        else:
            content += """
                <div class="section">
                    <h2>Файлы</h2>
                    <p>Нет прикреплённых файлов.</p>
                </div>
            """

        excavation_squares = data.get("excavation_squares", [])
        if excavation_squares:
            content += """
                <div class="section">
                    <h2>Территория исследования — поворотные точки</h2>
                    <ul>
            """
            for square in excavation_squares:
                content += f"""
                    <li>
                        <b>Координаты:</b> {square['geometry']}<br>
                        <b>Описание:</b> {square['geom_description']}
                    </li>
                """
            content += "</ul></div>"
        else:
            content += """
                <div class="section">
                    <h2>Территория исследования</h2>
                    <p>Нет поворотных точек.</p>
                </div>
            """

        return content

    def set_coordinate_to_point_list(self, row, lat, lon):

        item_lat = QTableWidgetItem(f"{lat:.6f}")
        item_lat.setFlags(item_lat.flags() & ~Qt.ItemIsEditable)
        # Создаём элемент таблицы для широты, форматируем до 6 знаков после запятой.
        # Делаем ячейку нередактируемой пользователем.

        item_lon = QTableWidgetItem(f"{lon:.6f}")
        item_lon.setFlags(item_lon.flags() & ~Qt.ItemIsEditable)
        # Аналогично создаём и настраиваем ячейку для долготы.

        self.view.pointsList.setItem(row, 0, item_lat)
        self.view.pointsList.setItem(row, 1, item_lon)
        # Устанавливаем созданные элементы (широту и долготу) в соответствующие ячейки строки `row`.

    def move_point(self, move_up: bool):
        '''
        если move_up = True, то ввеох поднимаем точку, 
        если move_up = False - вниз опускаем
        '''
        current_row = self.view.pointsList.currentRow()
        if current_row == -1:
            return  # Ничего не выбрано

        target_row = current_row - 1 if move_up else current_row + 1

        if target_row < 0 or target_row >= self.view.pointsList.rowCount():
            return  # Выход за границы

        # Сохраняем данные
        lat_current = self.view.pointsList.item(current_row, 0).text()
        lon_current = self.view.pointsList.item(current_row, 1).text()

        lat_target = self.view.pointsList.item(target_row, 0).text()
        lon_target = self.view.pointsList.item(target_row, 1).text()

        # Меняем строки местами
        self.view.pointsList.item(current_row, 0).setText(lat_target)
        self.view.pointsList.item(current_row, 1).setText(lon_target)

        self.view.pointsList.item(target_row, 0).setText(lat_current)
        self.view.pointsList.item(target_row, 1).setText(lon_current)

        # Перемещаем выделение
        self.view.pointsList.selectRow(target_row)
