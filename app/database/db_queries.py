class DataBaseQueries:
    def __init__(self):
        """Инициализация SQL-запросов (если нужно хранить что-то статическое — можно в self)."""
        pass

    @staticmethod
    def get_monuments():
        return """
            SELECT 
                m.monument_id,
                m.name,
                m.description,
                m.research_object,
                c.latitude,
                c.longitude,
                c.note
            FROM Monuments m
            LEFT JOIN Coordinates c ON m.monument_id = c.monument_id
        """

    @staticmethod
    def get_monument_by_id():
        return """
            SELECT 
                m.monument_id,
                m.name,
                m.description,
                m.research_object,
                c.latitude,
                c.longitude,
                c.note
            FROM Monuments m
            LEFT JOIN Coordinates c ON m.monument_id = c.monument_id
            WHERE m.monument_id = ?
        """

    @staticmethod
    def create_monument():
        return """
            INSERT INTO Monuments (name, description, research_object)
            VALUES (?, ?, ?)
        """

    @staticmethod
    def create_coordinate(fields_clause: str, placeholders: str):
        return f"""
            INSERT INTO Coordinates ({fields_clause})
            VALUES ({placeholders})
        """

    @staticmethod
    def update_monument_by_id(set_clause):
    
        return f"""
                UPDATE Monuments
                SET {set_clause}
                WHERE monument_id = ?
              """

    @staticmethod
    def get_coordinate_by_monument_id():
        return """
            SELECT latitude, longitude, note
            FROM Coordinates
            WHERE monument_id = ?
        """

    @staticmethod
    def get_coordinate_by_monument_id():
        
        return  """
                SELECT coord_id FROM Coordinates WHERE monument_id = ?
                """
    
    @staticmethod
    def update_coordinate_by_monument_id(set_clause):
        
        return  f"""
                    UPDATE Coordinates
                    SET {set_clause}
                    WHERE monument_id = ?
                """
    
    @staticmethod
    def create_coordinate_by_monument_id(fields_clause, placeholders):
        
        return  f"""
                    INSERT INTO Coordinates ({fields_clause})
                    VALUES ({placeholders})
                """

    @staticmethod
    def delete_monument_by_id():
        return  """
                DELETE FROM Monuments WHERE monument_id = ?
                """
    @staticmethod
    def get_monuments_query():
            """Возвращает SQL-запрос для выборки памятников с координатами."""
            return """
                SELECT 
                    m.monument_id,
                    m.name,
                    m.description,
                    m.research_object,
                    c.latitude,
                    c.longitude,
                    c.note
                FROM Monuments m
                LEFT JOIN Coordinates c ON m.monument_id = c.monument_id
            """

