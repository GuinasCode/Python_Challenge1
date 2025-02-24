import sqlite3

class Database:
    def __init__(self, db_name='restaurante.db'):
        self.db_name = db_name
    
    def connect(self):
        return sqlite3.connect(self.db_name)
    
    def execute_query(self, query, params=()):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()
        connection.close()
    
    def fetch_all(self, query, params=()):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        connection.close()
        return results
    
    
