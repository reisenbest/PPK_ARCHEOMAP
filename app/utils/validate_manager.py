class ValidateUILevelManager:
    
    """
    проверяет валидацию на уровне ui при вводе значений. 1 уровень проверки
    """
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def validate_create_method(self, monument_data: dict):
        """
        проверка для метода создания памятника
        """
        if 'name' not in monument_data or monument_data['name'].strip() == '':
            return False, "Имя памятника не может быть пустым view"
        if len(monument_data['name']) > 100:
            return False, "Имя слишком длинное (максимум 100 символов) view"
        if 'latitude' not in monument_data:
            return False, "Широта не может отсуствовать view"
        if 'longitude' not in monument_data:
            return False, "Долгота не может отсуствовать view"

        return True, ""

    def validate_read_method(self):
        pass

    def validate_update_method(self, monument_data: dict):
        """
        проверка для метода создания памятника
        """
        if 'name' not in monument_data or monument_data['name'].strip() == '':
            return False, "Имя памятника не может быть пустым"
        if len(monument_data['name']) > 100:
            return False, "Имя слишком длинное (максимум 100 символов) view"
        return True, ""

    def validate_delete_method(self):
        pass
