from utils import DatabaseManager
from pedido import Order

class Restaurate:
    def __init__(self):
        self.pedidos = []
       
    def getMenu(self):
        menu = Order.getMenu()
        return menu
  
    def makeOrder(self, cliente, itens):
        with DatabaseManager() as db:

            if isinstance(itens, str):    
                itens_ids = [int(item.strip()) for item in itens.split(",") if item.strip().isdigit()]
            elif isinstance(itens, list):
                itens_ids = [int(item) for item in itens if isinstance(item, (int, str)) and str(item).isdigit()]
            else:
                itens_ids = [int(itens)]

            if not itens_ids:
                print("Nenhum ID de item válido fornecido.")
                return

            placeholders = ",".join(["?"] * len(itens_ids))
            itens_encontrados = db.execute_query(f"SELECT id, item, valor FROM menu WHERE id IN ({placeholders})", itens_ids)
            
            if not itens_encontrados:
                print(f"Nenhum item encontrado para os IDs fornecidos: {itens_ids}")
                return

            itens_formatados = [f"{item[1]} (R$ {item[2]:.2f})" for item in itens_encontrados]  
            valor_total = sum(item[2] for item in itens_encontrados)

            db.execute_query('''
                INSERT INTO orders (data, nome_cliente, itens, status, valor_total)
                VALUES (date('now'), ?, ?, 'Pendente', ?);
            ''', (cliente, ", ".join(itens_formatados), valor_total))

            order_id = db.execute_query(
                '''SELECT id FROM orders
                ORDER BY id
                DESC LIMIT 1''')
            order_id = order_id[0][0]              

            mensagem = f"\nPedido {order_id} criado com sucesso para {cliente}. Total: R$ {valor_total:.2f}\n"
            return mensagem

    def statusUpdate(self, id):
        for pedido in self.pedidos:
            if pedido.id == id:
                pedido.statusUpdate()
                return f"Pedido {id} atualizado para {pedido.status}"
        return "Número do pedido incorreto."

    def listOrders(self):
        return [pedido.orderStatus() for pedido in self.pedidos]
    
    def listPendingOrders(self):
        return [pedido.orderStatus() for pedido in self.pedidos if pedido.status != "Entregue"]
    
    def dailyRevenue(self):
        return sum(pedido.valor_total for pedido in self.pedidos if pedido.status == "Entregue")

""" if __name__ == "__main__":
    database = Database()
    pedidos = database.fetch_all('''SELECT * FROM orders;''')
    print(pedidos) """
