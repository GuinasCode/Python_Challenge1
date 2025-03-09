import sqlite3

def create_tables():
    connection = sqlite3.connect('restaurante.db')
    cursor = connection.cursor()

    cursor.executescript(
        '''CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data DATE NOT NULL,
            nome_cliente TEXT NOT NULL,
            itens TEXT NOT NULL,
            status TEXT NOT NULL,
            valor_total REAL NOT NULL
            );
        
        CREATE TABLE menu (
            id INTEGER PRIMARY KEY,
            item TEXT NOT NULL,
            valor REAL NOT NULL);

        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            login TEXT NOT NULL,
            nome TEXT NOT NULL,
            email TEXT NOT NULL);
        ''')

    connection.commit()
    connection.close()

if __name__ == '__main__':
    create_tables()
    print('Banco de dados e tabelas inicializados com sucesso!')