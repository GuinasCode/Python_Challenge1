
from datetime import datetime
import sqlite3

status = ["Pendente","Em prepapro", "Pronto","Entregue"]

class idGenerator:
        idPedido = {}
    
        @classmethod    
        def gerarId(cls):
            data_atual = datetime.now().strftime("%y%m%d")
            cls.idPedido[data_atual] = cls.idPedido.get(data_atual, 0) + 1
        
            indice = f"{cls.idPedido[data_atual]:02d}"
            return f"{data_atual}{indice}"

class DatabaseManager:
    def __init__(self, db_name="restaurante.db"):
        self.db_name = db_name
        self.connection = None
        self.cursor = None
    
    def connect(self):
        self.connection = sqlite3.connect(self.db_name)
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