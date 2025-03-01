from datetime import datetime
import sqlite3
import os

status = ["Pendente","Em prepapro", "Pronto","Entregue"]

class DatabaseManager:
    def __init__(self, db_name="restaurante.db"):
        self.db_name = db_name
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, db_name)
        self.connection = None
        self.cursor = None
    
    def connect(self):
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        return self
    
    def  execute_query(self, query, params=None):
        if not self.connection:
            self.connect()
        
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        
        return self.cursor.fetchall()

    def execute_many(self, query, params_list):
        if not self.connection:
            self.connect()
        
        self.cursor.executemany(query, params_list)
        return self.cursor
    
    def commit(self):
        if self.connection:
           self.connection.commit()
        return self

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None

    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.close()