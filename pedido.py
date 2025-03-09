from utils import status, DatabaseManager
from datetime import datetime

class Order:

    def __init__(self,
                 id=None,
                 cliente=None, 
                 itens=None, 
                 status="Pendente", 
                 valor_total=None, 
                 data=None):
        self.id = id
        self.cliente = cliente
        self.itens = itens
        self.status = status
        self.valor_total = valor_total
        self.data = datetime.today().strftime('%Y-%m-%d')

    @staticmethod
    def getMenu():
        with DatabaseManager() as db: 
            menu = db.execute_query('''SELECT * FROM menu;''')
            return menu
     
    def new_order(self):
        total = 0
        itens_formatados = []

        with DatabaseManager() as db:
            for item_id in self.itens:
                item_id = item_id.strip()
                if not item_id:
                    continue
                item_info = db.execute_query('SELECT item, valor FROM menu WHERE ID = ?', (item_id,))
                if item_info:
                    nome_item, preco = item_info[0]
                    total += preco
                    itens_formatados.append(f"{nome_item} (R$ {preco:.2f})")
            
            if not itens_formatados:
                return "Nenhum item válido encontrado. Pedido não criado."
            
            self.itens = ", ".join(itens_formatados)
            self.valor_total = total
            with DatabaseManager() as db:
                db.execute_query('''
                INSERT INTO orders (data, nome_cliente, itens, status, valor_total)
                VALUES (?, ?, ?, ?, ?);
                ''', (self.data, self.cliente, self.itens, self.status, self.valor_total))
                order_id = db.execute_query('SELECT id FROM orders ORDER BY id DESC LIMIT 1')
                self.id = order_id[0][0]
            return f"\nPedido {self.id} criado com sucesso para {self.cliente}. Total: R$ {self.valor_total:.2f}\n"
    
    @staticmethod
    def check_order(order_id):
        with DatabaseManager() as db:
            order = db.execute_query('SELECT status FROM orders WHERE id = ?', (order_id,))
            if not order:
                return f"Nenhum pedido encontrado com id {order_id}"
            return order[0][0]
    
    @staticmethod
    def update_status(order_id):
        with DatabaseManager() as db:
            order = Order.check_order(order_id)
            if not order:
                return f"Pedido {order_id} não encontrado."
            index = status.index(order)
            if index == 3:
                return "\nPedido finalizado, não é possível alterar o status\n"
            
            order_status = status[index +1]
            with DatabaseManager() as db:
                db.execute_query('UPDATE orders SET status = ? WHERE ID = ?', (order_status, order_id))
            
            return f"\nPedido {order_id} atualizado para {order_status}\n"
        
    @staticmethod
    def list_orders(date=None):
        if not date:
            date = datetime.today().strftime("%Y-%m-%d")
        else:
            date = datetime.strptime(date, "%d/%m/%Y").strftime("%Y-%m-%d")
        
        with DatabaseManager() as db:
            orders = db.execute_query('SELECT * FROM orders WHERE data = ?', (date,))
        
        if not orders:
            return "Nenhum pedido cadastrado nesta data."
        
        formatted_orders = [f"\n=== Pedidos de {datetime.strptime(date, '%Y-%m-%d').strftime('%d/%m/%Y')} ==="]

        for order in orders:
            order_id, data, nome_cliente, itens, status, valor_total = order
            itens_formatados = "\n - ".join(itens.split(", "))

            formatted_orders.append(
                f"\nPedido ID: {order_id}\n"
                f"\nCliente: {nome_cliente}\n"
                f"\nItens do Pedido:\n - {itens_formatados}\n"
                f"\nStatus: {status}\n"
                f"\nValor Total: R$ {valor_total:.2f}\n"
                f"{'-'*30}"
            )
        return "\n".join(formatted_orders)

    @staticmethod
    def list_all_orders():
        
        with DatabaseManager() as db:
            orders = db.execute_query('SELECT * FROM orders')
        
        if not orders:
            return "\nNenhum pedido cadastrado."
        
        formatted_orders = [f"\n=== Lista de Pedidos ==="]

        for order in orders:
            order_id, data, nome_cliente, itens, status, valor_total = order
            itens_formatados = "\n - ".join(itens.split(", "))

            formatted_orders.append(
                f"\nPedido ID: {order_id}"
                f"\nData do Pedido: {datetime.strptime(data, '%Y-%m-%d').strftime('%d/%m/%Y')}"
                f"\nCliente: {nome_cliente}"
                f"\nItens do Pedido:\n - {itens_formatados}"
                f"\nStatus: {status}"
                f"\nValor Total: R$ {valor_total:.2f}\n"
                f"{'-'*30}"
            )
        return "\n".join(formatted_orders)

    @staticmethod
    def list_pending_orders():
        with DatabaseManager() as db:
            orders = db.execute_query('SELECT * FROM orders WHERE status != "Entregue"')

        if not orders:
            return "\nNenhum pedido pendente"
        
        formatted_orders = [f"\n=== Lista de Pedidos ==="]

        for order in orders: 
            order_id, data, nome_cliente, itens, status, valor_total = order
            itens_formatados = "\n - ".join(itens.split(", "))
            
            formatted_orders.append(
                f"\nPedido ID: {order_id}"
                f"\nData do Pedido: {datetime.strptime(data, '%Y-%m-%d').strftime('%d/%m/%Y')}"
                f"\nCliente: {nome_cliente}"
                f"\nItens do Pedido:\n - {itens_formatados}"
                f"\nStatus: {status}"
                f"\nValor Total: R$ {valor_total:.2f}\n"
                f"{'-'*30}"
            )
        return "\n".join(formatted_orders)

    @staticmethod
    def get_revenue(start_date=None, end_date=None):
        with DatabaseManager() as db:
            if not start_date and not end_date:
                revenue = db.execute_query('''SELECT SUM(valor_total) AS receita_hoje
                                           FROM orders
                                           WHERE data = DATE('now');
                                            ''')
                revenue = revenue[0][0] if revenue[0][0] else 0
                return f"\nA receita total de hoje foi de R$ {revenue:.2f}\n"
            
            if not end_date:
                end_date = start_date
            
            try:
                inicio = datetime.strptime(start_date, "%d/%m/%Y").strftime("%Y-%m-%d")
                fim = datetime.strptime(end_date, "%d/%m/%Y").strftime("%Y-%m-%d")
            except ValueError:
                return "\nErro: Formato de data inválido. Use DD/MM/YYYY.\n"
            query = '''SELECT SUM(valor_total) AS receita
                        FROM orders
                        WHERE data BETWEEN ? AND ? 
                    '''
            revenue = db.execute_query(query, (inicio, fim))
            revenue = revenue[0][0] if revenue[0][0] else 0
            return f"\nA receita total entre {start_date} e {end_date} hoje foi de R$ {revenue:.2f}\n"