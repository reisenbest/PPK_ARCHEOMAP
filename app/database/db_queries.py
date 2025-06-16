#здесь собраны кверики для скл чтобы не утяжелять код...хотя он итак тяжелый



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
    def get_monument_by_id_query():
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
    def get_files_by_monument_id_query():
        return """
            SELECT 
                file_id,
                file_path,
                file_type,
                file_description,
                monument_id
            FROM Files
            WHERE monument_id = ?
            """
    
    @staticmethod
    def get_excavation_squares_by_monument_id_query():
        return """
            SELECT 
                square_id,
                geometry,
                geom_description,
                monument_id
            FROM ExcavationSquares
            WHERE monument_id = ?
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
    def create_file():
        return """
            INSERT INTO Files (file_path, file_type, file_description, monument_id)
            VALUES (?, ?, ?, ?)
        """
    
    @staticmethod
    def create_excavation_square():
        return """
            INSERT INTO ExcavationSquares (geometry, geom_description, monument_id)
            VALUES (?, ?, ?, ?)
        """

    @staticmethod
    def update_monument_by_id(set_clause):
    
        return f"""
                UPDATE Monuments
                SET {set_clause}
                WHERE monument_id = ?
              """
    #FIXME: два одинаковых метода, оставить один
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
    def create_monument_list_view():
        """Возвращает SQL-запрос для отображения данных из БД в окне monument_list в табличном виде."""
        return """
            SELECT 
                m.monument_id AS "ID",
                m.name AS "Название",
                m.description AS "Описание",
                m.research_object AS "Объект исследования",
                c.latitude AS "Широта",
                c.longitude AS "Долгота",
                c.note AS "Примечание"
            FROM Monuments m
            LEFT JOIN Coordinates c ON m.monument_id = c.monument_id
            """
    
    @staticmethod
    def get_files_for_monument_by_monument_id():
        return """
        SELECT file_id, file_path, file_type, file_description 
        FROM Files 
        WHERE monument_id = ?
        """
    @staticmethod
    def get_file_path_by_id():
        return '''SELECT file_path FROM Files WHERE file_id = ?'''
    @staticmethod
    def delete_file_by_id():
        return '''DELETE FROM Files WHERE file_id = ?'''
    
    @staticmethod
    def insert_file():
        return '''
            INSERT INTO Files (file_path, file_type, file_description, monument_id)
            VALUES (?, ?, ?, ?)
            '''
    @staticmethod
    def update_file_paths_query():
        return '''
            UPDATE files SET file_path = ? WHERE file_id = ?
        '''
    
    #TODO:

    @staticmethod
    def get_excavation_squares_for_monument_by_monument_id():
        return """
        SELECT square_id, geometry, geom_description
        FROM ExcavationSquares 
        WHERE monument_id = ?
        """
    @staticmethod
    def get_excavation_square_by_id():
        return '''SELECT geometry, geom_description  FROM Files WHERE square_id = ?'''
    
    @staticmethod
    def delete_excavation_square_by_id():
        return '''DELETE FROM ExcavationSquares WHERE square_id = ?'''
    
    @staticmethod
    def create_excavation_square_by_monument_id():
        return"""
            INSERT INTO ExcavationSquares (geometry, geom_description, monument_id)
            VALUES (?, ?, ?)
            """

    # @staticmethod
    # def insert_file():
    #     return '''
    #         INSERT INTO Files (file_path, file_type, file_description, monument_id)
    #         VALUES (?, ?, ?, ?)
    #         '''
    # @staticmethod
    # def update_file_paths_query():
    #     return '''
    #         UPDATE files SET file_path = ? WHERE file_id = ?
    #     '''


    