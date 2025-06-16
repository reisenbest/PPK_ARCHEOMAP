
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



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

class PutExcavationSquaresView(QDialog, BaseView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.load_ui('excavation_squares_manage_window.ui')
        self.setWindowModality(Qt.ApplicationModal)  # Блокирует все окна приложения
        


class PutExcavationSquaresController(QObject):
    
    square_saved = pyqtSignal()

    def __init__(self, monument_id, db_manager, parent=None):
        super().__init__(parent)
        self.view = PutExcavationSquaresView(parent)  # ← передай родителя
        self.monument_id = monument_id
        self.db_manager = db_manager
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


        # Настройка колонок таблицы
        self.view.pointsList.setColumnCount(2)
        self.view.pointsList.setHorizontalHeaderLabels(['Latitude', 'Longitude'])

        # Настройка поведения при выделении строк 
        self.view.pointsList.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.view.pointsList.setSelectionMode(QAbstractItemView.SingleSelection)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         


        
    def show(self):
        self.clear_view_data()
        self.view.show()



    def add_point_button(self, arg):
        # TODO: добавить валидацию для полей спинбоксов
        lat = self.view.latSpinBox.value()
        lon = self.view.lonSpinBox.value()

        row = self.view.pointsList.rowCount()
        self.view.pointsList.insertRow(row)

        item_lat = QTableWidgetItem(f"{lat:.6f}")
        item_lat.setFlags(item_lat.flags() & ~Qt.ItemIsEditable)

        item_lon = QTableWidgetItem(f"{lon:.6f}")
        item_lon.setFlags(item_lon.flags() & ~Qt.ItemIsEditable)

        self.view.pointsList.setItem(row, 0, item_lat)
        self.view.pointsList.setItem(row, 1, item_lon)

    def remove_point_button(self, arg):
        selected_items = self.view.pointsList.selectedItems()
        if not selected_items:
            return

        # Получаем индекс строки первого выбранного элемента
        row = self.view.pointsList.row(selected_items[0])
        self.view.pointsList.removeRow(row)

        self.update_buttons_state()  # Обновить состояние кнопок после удаления

    def move_up_point_button(self, arg):
        # TODO: сделать функцию из этого
        current_row = self.view.pointsList.currentRow()
        if current_row <= 0:
            return  # Уже наверху или ничего не выбрано

        # Сохраняем данные текущей и предыдущей строки
        lat_current = self.view.pointsList.item(current_row, 0).text()
        lon_current = self.view.pointsList.item(current_row, 1).text()

        lat_above = self.view.pointsList.item(current_row - 1, 0).text()
        lon_above = self.view.pointsList.item(current_row - 1, 1).text()

        # Меняем строки местами
        self.view.pointsList.item(current_row, 0).setText(lat_above)
        self.view.pointsList.item(current_row, 1).setText(lon_above)

        self.view.pointsList.item(current_row - 1, 0).setText(lat_current)
        self.view.pointsList.item(current_row - 1, 1).setText(lon_current)

        # Перемещаем выделение
        self.view.pointsList.selectRow(current_row - 1)

    def move_down_point_button(self, arg):
        # TODO: сделать функцию из этого
        current_row = self.view.pointsList.currentRow()
        if current_row == -1 or current_row >= self.view.pointsList.rowCount() - 1:
            return  # Уже внизу или ничего не выбрано

        # Сохраняем данные текущей и следующей строки
        lat_current = self.view.pointsList.item(current_row, 0).text()
        lon_current = self.view.pointsList.item(current_row, 1).text()

        lat_below = self.view.pointsList.item(current_row + 1, 0).text()
        lon_below = self.view.pointsList.item(current_row + 1, 1).text()

        # Меняем строки местами
        self.view.pointsList.item(current_row, 0).setText(lat_below)
        self.view.pointsList.item(current_row, 1).setText(lon_below)

        self.view.pointsList.item(current_row + 1, 0).setText(lat_current)
        self.view.pointsList.item(current_row + 1, 1).setText(lon_current)

        # Перемещаем выделение
        self.view.pointsList.selectRow(current_row + 1)

    def update_point_button(self, arg):
        current_row = self.view.pointsList.currentRow()
        if current_row == -1:
            return  # Ничего не выбрано

        lat = self.view.latSpinBox.value()
        lon = self.view.lonSpinBox.value()

        item_lat = QTableWidgetItem(f"{lat:.6f}")
        item_lat.setFlags(item_lat.flags() & ~Qt.ItemIsEditable)

        item_lon = QTableWidgetItem(f"{lon:.6f}")
        item_lon.setFlags(item_lon.flags() & ~Qt.ItemIsEditable)

        self.view.pointsList.setItem(current_row, 0, item_lat)
        self.view.pointsList.setItem(current_row, 1, item_lon)

    def cancel_button(self):
        print(self.monument_id)
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

        # Проверка на минимум 3 точки (для полигона)
        if len(points) < 3:
            QMessageBox.warning(self.view, "Недостаточно точек", "Полигон должен содержать как минимум 3 точки.")
            return

        # Замыкаем контур
        if points[0] != points[-1]:
            points.append(points[0])

        # Формируем GeoJSON Polygon
        geojson_obj = {
            "type": "Polygon",
            "coordinates": [points]
        }

        # Получаем описание
        geometry = json.dumps(geojson_obj, indent=2, ensure_ascii=False)
        description = self.view.descriptionEdit.toPlainText()

        data = {'geometry': geometry,
                'geom_description': description,
                'monument_id': self.monument_id} 
        



        # Печатаем результат
        print("=== GEOMETRY ===")
        print(geometry)

        print("\n=== GEOM DESCRIPTION ===")
        print(description)

        # Можно также временно показывать пользователю
        QMessageBox.information(self.view, "GeoJSON сформирован", "GeoJSON и описание выведены в консоль.")

        self.db_manager.excavation_squares_table.create_excavation_squares_by_monument_id(data=data)
        self.square_saved.emit()
        self.view.accept()  # можно закрыть диалог после сохранения


    def update_buttons_state(self):
        selected = self.view.pointsList.selectedItems()
        has_selection = bool(selected)

        self.view.updatePointBtn.setEnabled(has_selection)
        self.view.removePointBtn.setEnabled(has_selection)
        self.view.moveUpBtn.setEnabled(has_selection)
        self.view.moveDownBtn.setEnabled(has_selection)
    
    def clear_view_data(self):
        self.view.latSpinBox.setValue(0.0)
        self.view.lonSpinBox.setValue(0.0)
        self.view.descriptionEdit.clear()
        self.view.pointsList.setRowCount(0)  # Очищает все строки таблицы
        self.update_buttons_state()