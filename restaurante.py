from database import Database
from pedido import Order

class Restaurate:
    def __init__(self):
        self.pedidos = []
    
    def makeOrder(self, cliente, itens):
        db = Database()
        connection = db.connect()
        cursor = connection.cursor()

    # Verifica o tipo de entrada e converte para uma lista de IDs
        if isinstance(itens, str):    
            itens_ids = [int(item.strip()) for item in itens.split(",") if item.strip().isdigit()]
        elif isinstance(itens, list):
            itens_ids = [int(item) for item in itens if isinstance(item, (int, str)) and str(item).isdigit()]
        else:
            itens_ids = [int(itens)]

        if not itens_ids:
            print("Nenhum ID de item válido fornecido.")
            connection.close()
            return

        # Criar a query para buscar os itens pelo ID
        placeholders = ",".join(["?"] * len(itens_ids))
        cursor.execute(f"SELECT id, item, valor FROM menu WHERE id IN ({placeholders})", itens_ids)
        itens_encontrados = cursor.fetchall()

        if not itens_encontrados:
            print(f"Nenhum item encontrado para os IDs fornecidos: {itens_ids}")
            connection.close()
            return

        # Formatar os itens e calcular o valor total
        itens_formatados = [f"{item[1]} (R$ {item[2]:.2f})" for item in itens_encontrados]  
        valor_total = sum(item[2] for item in itens_encontrados)

        # Inserir pedido no banco de dados
        cursor.execute('''
            INSERT INTO orders (data, nome_cliente, itens, status, valor_total)
            VALUES (date('now'), ?, ?, 'Pendente', ?);
        ''', (cliente, ", ".join(itens_formatados), valor_total))

        order_id = cursor.lastrowid  # Obtém o ID do pedido recém-criado

        connection.commit()
        connection.close()

        mensagem = f"\nPedido {order_id} criado com sucesso para {cliente}. Total: R$ {valor_total:.2f}\n"
        return mensagem
         
    def getMenu(self):
        menu = Order.getMenu()
        return menu
    
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

if __name__ == "__main__":
    database = Database()
    pedidos = database.fetch_all('''SELECT * FROM orders;''')
    print(pedidos)
