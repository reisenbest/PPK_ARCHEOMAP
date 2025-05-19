Карты режутся на тайлы и кушаются лифлетом и пр. в формате  EPSG: 3857
это координаты в формате Оси: X и Y в метрах от экватора и Гринвича.
Пример: 3373000, 8400000 — в метрах.

Используется: OpenStreetMap, Google Maps, Leaflet, карты в вебе.


координаты общепринятые (широта долгота в градусах) - EPSG:4326 — Географические координаты (WGS 84)
Оси: Широта (latitude), долгота (longitude), в градусах.

Пример: 60.003, 30.305 — в градусах.

Используется: GPS, геоданные, GeoJSON, и др.


чтобы они корректно отображались на подложке в формате EPSG: 3857 при их загрузке нужно проводить 
конвертацию




pyuic5 {filename}.ui -o {filename}.py - в терминал строку - создание из qtDesigner файла файла на питоне


🔚 Итоговая рекомендация по архитектуре:
MainWindow — главный класс окна.

MapBridge — класс связи JS ↔ Python.

DatabaseManager — отдельный класс для работы с SQLite.

PointModel — класс, представляющий точку (заголовок, описание, координаты и пути к медиа).

AddPointDialog, DetailsDialog — отдельные компоненты/окна.

map.html и JS-функции — вызываются из Python через runJavaScript.


app/
├── main.py
├── config/
│   └── settings.json             # Настройки приложения
├── ui/                           # .ui файлы, созданные в Qt Designer
│   ├── main_menu.ui
│   ├── map_window.ui
│   ├── details_dialog.ui
│   ├── add_point_dialog.ui
│   └── settings_dialog.ui
├── views/                        # Интерфейсные классы (Qt + логика отображения)
│   ├── main_menu.py              # Главное меню (загружает main_menu.ui)
│   ├── map_window.py
│   ├── details_dialog.py
│   ├── add_point_dialog.py
│   └── settings_dialog.py
├── models/                       # Модели данных и базы
│   ├── point.py
│   └── database.py
├── map/                          # Карта (leaflet, QWebEngineView)
│   ├── map_widget.py
│   ├── map.html                  # Сам html-шаблон карты
│   └── leaflet/                  # Локальные файлы Leaflet (JS/CSS/tiles)
├── media/                    # Статика
│   ├── icons/
│   ├── images/
│   └── pdfs/
├── utils/                        # Утилиты, загрузчики вспомогательные классы
│   └── helpers.py
└── README.md



разработать и внедрить БД 

написать исключения и валидацию скл и ui для всех методов 