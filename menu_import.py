import sqlite3
from menu import MENU

def insert_menu():
    connection = sqlite3.connect('restaurante.db')
    cursor = connection.cursor()

    for item in MENU:
            
        cursor.execute('''
            INSERT INTO menu (id, item, valor)
            VALUES (?, ?, ?)
            ''', (item["id"], item["nome"], item["preco"]))
    
    connection.commit()
    connection.close()
    print("Itens do menun importados com sucesso!")

if __name__ == "__main__":
    insert_menu()