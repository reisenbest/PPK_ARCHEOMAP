
import os
import sys
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QObject
from PyQt5.uic import loadUi
from utils.base_classes import BaseView
import config
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QAbstractItemView
import json
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMessageBox
from utils.utils import UtilsForViews



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

class PutExcavationSquaresView(QDialog, BaseView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.load_ui('excavation_squares_manage_window.ui')
        self.setWindowModality(Qt.ApplicationModal)  # Блокирует все окна приложения
        


class PutExcavationSquaresController(QObject):
    
    square_saved = pyqtSignal()

    def __init__(self, monument_id, db_manager, existing_data=None, parent=None):
        super().__init__(parent)
        self.view = PutExcavationSquaresView(parent)
        
        self.db_manager = db_manager
        self.utils = UtilsForViews(view=self.view)
        
        self.monument_id = monument_id
        self.existing_data = existing_data  # ← новый параметр
        self.square_id = existing_data.get('square_id') if existing_data else None  # предполагается наличие ID

        self.setup_connections()

        self.view.updatePointBtn.setEnabled(False)
        self.view.removePointBtn.setEnabled(False)
        self.view.moveUpBtn.setEnabled(False)
        self.view.moveDownBtn.setEnabled(False)




    def setup_connections(self):
        self.view.cancelBtn.clicked.connect(self.cancel_button)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
        self.view.saveBtn.clicked.connect(self.save_button)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
        self.view.addPointBtn.clicked.connect(self.add_point_button)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
        self.view.removePointBtn.clicked.connect(self.remove_point_button)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
        self.view.moveUpBtn.clicked.connect(self.move_up_point_button)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
        self.view.moveDownBtn.clicked.connect(self.move_down_point_button)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
        self.view.updatePointBtn.clicked.connect(self.update_point_button)
        self.view.pointsList.itemSelectionChanged.connect(self.update_buttons_state)
        self.view.pointsList.itemSelectionChanged.connect(self.update_spin_boxes_values)


        # Настройка колонок таблицы
        self.view.pointsList.setColumnCount(2)
        self.view.pointsList.setHorizontalHeaderLabels(['Latitude', 'Longitude'])
        
        #если передали данные существующщей записи с полигонами - запускаем редактирование иначе создание
        if self.existing_data:
            self.load_existing_data()

        # Настройка поведения при выделении строк 
        self.view.pointsList.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.view.pointsList.setSelectionMode(QAbstractItemView.SingleSelection)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         


        
    def show(self):
        #если не передаются даныне полигона для редактирования - очищаем окно от предыдщуих операций 
        if not self.existing_data:
            self.clear_view_data()
            self.view.show()
        else:
            #иначе передаем и показываем вместе с данными которые надо отредактировать
            self.view.show()



    def add_point_button(self):
        # TODO: добавить валидацию для полей спинбоксов
        # (Здесь стоит реализовать проверку введённых значений, например: диапазон широт/долгот, не нули и т.д.)

        row = self.view.pointsList.rowCount()
        # Получаем текущее количество строк в таблице — новая точка будет добавлена в конец.

        self.view.pointsList.insertRow(row)
        # Вставляем новую (пустую) строку в таблицу на позицию row.

        lat = self.view.latSpinBox.value()
        lon = self.view.lonSpinBox.value()
        # Считываем значения широты и долготы из соответствующих spinbox-ов на форме.

        self.utils.set_coordinate_to_point_list(row=row, lat=lat, lon=lon)

        # Очищаем (сбрасываем в 0.0) значения spinbox-ов, чтобы пользователь мог вводить новые координаты.
        self.view.latSpinBox.setValue(0.0)
        self.view.lonSpinBox.setValue(0.0)



    def update_point_button(self, arg):
        current_row = self.view.pointsList.currentRow()
        if current_row == -1:
            return  # Ничего не выбрано

        lat = self.view.latSpinBox.value()
        lon = self.view.lonSpinBox.value()
        # Считываем значения широты и долготы из соответствующих spinbox-ов на форме.

        self.utils.set_coordinate_to_point_list(row=current_row, lat=lat, lon=lon)

        

    def remove_point_button(self, arg):
        selected_items = self.view.pointsList.selectedItems()
        if not selected_items:
            return

        # Получаем индекс строки первого выбранного элемента
        row = self.view.pointsList.row(selected_items[0])
        self.view.pointsList.removeRow(row)

        self.update_buttons_state()  # Обновить состояние кнопок после удаления

    def move_up_point_button(self):
        self.utils.move_point(move_up=True)

    def move_down_point_button(self):
        self.utils.move_point( move_up=False)

    def update_buttons_state(self):
        selected = self.view.pointsList.selectedItems()
        has_selection = bool(selected)

        self.view.updatePointBtn.setEnabled(has_selection)
        self.view.removePointBtn.setEnabled(has_selection)
        self.view.moveUpBtn.setEnabled(has_selection)
        self.view.moveDownBtn.setEnabled(has_selection)
        
    def update_spin_boxes_values(self):
        selected = self.view.pointsList.selectedItems()
        if not selected:
        # Нет выделенных элементов — можно очистить спинбоксы или оставить как есть
            return

        # Получаем индекс строки выделенного элемента (берём первую выбранную ячейку)
        row = self.view.pointsList.row(selected[0])

        item_lat = self.view.pointsList.item(row, 0)
        item_lon = self.view.pointsList.item(row, 1)

        if item_lat and item_lon:
            try:
                lat = float(item_lat.text())
                lon = float(item_lon.text())
                self.view.latSpinBox.setValue(lat)
                self.view.lonSpinBox.setValue(lon)
            except ValueError:
                # Если текст не конвертируется в float — игнорируем
                pass
    

    
    def cancel_button(self):
        self.view.reject()

    def save_button(self):
        # Собираем точки из таблицы
        points = []
        for row in range(self.view.pointsList.rowCount()):
            lat_item = self.view.pointsList.item(row, 0)
            lon_item = self.view.pointsList.item(row, 1)
            if lat_item and lon_item:
                try:
                    lat = float(lat_item.text())
                    lon = float(lon_item.text())
                    points.append([lon, lat])  # GeoJSON: [долгота, широта]
                except ValueError:
                    QMessageBox.warning(self.view, "Неверные данные", f"Строка {row + 1} содержит недопустимые координаты.")
                    return

        if len(points) < 3:
            QMessageBox.warning(self.view, "Недостаточно точек", "Полигон должен содержать как минимум 3 точки.")
            return
        
        #добавляет точку, дублирующую первую (типо так принято в geojson)
        if points[0] != points[-1]:
            points.append(points[0])

        geojson_obj = {
            "type": "Polygon",
            "coordinates": [points]
        }

        geometry = json.dumps(geojson_obj, indent=2, ensure_ascii=False)
        description = self.view.descriptionEdit.toPlainText()

        data = {
            'geometry': geometry,
            'geom_description': description,
            'monument_id': self.monument_id
        }

        try:
            if self.square_id:
                # Обновление существующей записи
                self.db_manager.excavation_squares_table.update_excavation_square_by_id(
                    square_id=self.square_id,
                    square_data=data
                )
            else:
                # Создание новой записи
                
                self.db_manager.excavation_squares_table.create_excavation_squares_by_monument_id(data=data)

            self.square_saved.emit()
            self.view.accept()

        except Exception as e:
            QMessageBox.critical(self.view, "Ошибка сохранения", f"Не удалось сохранить полигон: {e}")

        # Можно также временно показывать пользователю
        QMessageBox.information(self.view, "GeoJSON сформирован", "данные записаны")


        self.square_saved.emit()
        self.view.accept()  # можно закрыть диалог после сохранения



    def clear_view_data(self):
        self.view.latSpinBox.setValue(0.0)
        self.view.lonSpinBox.setValue(0.0)
        self.view.descriptionEdit.clear()
        self.view.pointsList.setRowCount(0)  # Очищает все строки таблицы
        self.update_buttons_state()

    
    def load_existing_data(self):
        try:
            geometry = json.loads(self.existing_data['geometry'])
            points = geometry.get("coordinates", [[]])[0]

            # Удаляем последнюю точку, если она дублирует первую (GeoJSON замкнутый полигон)
            if len(points) > 1 and points[0] == points[-1]:
                points = points[:-1]


            for lon, lat in points:
                row = self.view.pointsList.rowCount()
                self.view.pointsList.insertRow(row)

                self.utils.set_coordinate_to_point_list(row=row, lat=lat, lon=lon)

        
            self.view.descriptionEdit.setPlainText(self.existing_data.get('geom_description', ''))

        except Exception as e:
            QMessageBox.critical(self.view, "Ошибка загрузки", f"Не удалось загрузить существующие данные: {e}")