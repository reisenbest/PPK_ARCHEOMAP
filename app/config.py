import os



#здесь собраны глобальные переменные для проекта
# Корень проекта — директория, где лежит config.py
BASE_APP_DIR = os.path.dirname(os.path.abspath(__file__))


UI_DIR = os.path.join(BASE_APP_DIR, "ui")
MAP_DIR = os.path.join(BASE_APP_DIR, "map")
MEDIA_DIR = os.path.join(BASE_APP_DIR, "media")
DATABASE_DIR = os.path.join(BASE_APP_DIR, "database")
UTILS_DIR = os.path.join(BASE_APP_DIR, "utils")
VIEWS_DIR = os.path.join(BASE_APP_DIR, "views")




for path in [UI_DIR, MAP_DIR, MEDIA_DIR, DATABASE_DIR, UTILS_DIR, VIEWS_DIR]:
    if not os.path.isdir(path):
        raise FileNotFoundError(f"⚠️  Warning: Directory not found — {path}")
    
