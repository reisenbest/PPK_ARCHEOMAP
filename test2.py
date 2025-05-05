import sys
import os
import math
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsEllipseItem
from PyQt5.QtGui import QPixmap, QBrush, QColor
from PyQt5.QtCore import Qt

TILE_SIZE = 256
ZOOM = 15

# Центр карты (широта и долгота)
CENTER_LAT = 59.9500
CENTER_LON = 30.3167

class TileMapViewer(QGraphicsView):
    def __init__(self, tile_dir, zoom=15, parent=None):
        super().__init__(parent)
        self.tile_dir = tile_dir
        self.zoom = zoom
        self.tile_size = TILE_SIZE

        self._scale_factor = 1.15  # Коэффициент зума

        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setDragMode(QGraphicsView.ScrollHandDrag)

        self.load_tiles()
        self.add_geo_point(59.9500, 30.3167, "red")

    def wheelEvent(self, event):
        """Обработка колесика мыши для зума"""
        if event.angleDelta().y() > 0:
            self.scale(self._scale_factor, self._scale_factor)
        else:
            self.scale(1 / self._scale_factor, 1 / self._scale_factor)

    def load_tiles(self):
        z_path = os.path.join(self.tile_dir, str(self.zoom))
        if not os.path.exists(z_path):
            print("Тайл-зум не найден:", z_path)
            return

        for x in os.listdir(z_path):
            x_path = os.path.join(z_path, x)
            if not os.path.isdir(x_path): continue

            for y_file in os.listdir(x_path):
                if not y_file.endswith('.png'): continue

                y = y_file.split('.')[0]
                tile_path = os.path.join(x_path, y_file)
                pixmap = QPixmap(tile_path)

                item = QGraphicsPixmapItem(pixmap)
                item.setPos(int(x) * self.tile_size, int(y) * self.tile_size)
                self.scene.addItem(item)

    def add_geo_point(self, lat, lon, color="blue"):
        """Добавляет точку, заданную в широте и долготе (EPSG:4326)"""
        x_tile_f, y_tile_f = self.latlon_to_tile_coords(lat, lon, self.zoom)
        x_pix = x_tile_f * self.tile_size
        y_pix = y_tile_f * self.tile_size

        ellipse_size = 10
        ellipse = QGraphicsEllipseItem(x_pix - ellipse_size / 2, y_pix - ellipse_size / 2, ellipse_size, ellipse_size)
        ellipse.setBrush(QBrush(QColor(color)))
        ellipse.setZValue(10)
        self.scene.addItem(ellipse)

    def latlon_to_tile_coords(self, lat, lon, zoom):
        """Конвертация координат (EPSG:4326) в тайловые координаты (float)"""
        lat_rad = math.radians(lat)
        n = 2.0 ** zoom
        x_tile = (lon + 180.0) / 360.0 * n
        y_tile = (1.0 - math.log(math.tan(lat_rad) + 1 / math.cos(lat_rad)) / math.pi) / 2.0 * n
        return x_tile, y_tile

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = TileMapViewer("OSM/tiles2", zoom=ZOOM)
    viewer.resize(1024, 768)
    viewer.show()
    sys.exit(app.exec_())
