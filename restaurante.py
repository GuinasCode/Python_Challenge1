# Gerencia os pedidos (adicionar, atualizar, listar, etc)
from menu import MENU
from pedido import Order

class Restaurate:
    def __init__(self):
        self.pedidos = []
    
    def makeOrder(self, cliente, itens):
        """Cria um novo pedido e adiciona à lista."""
        pedido = Order(cliente, itens)
        self.pedidos.append(pedido)
        return pedido.id
    
    def statusUpdate(self, id):
        """Atualiza o status do pedido."""
        for pedido in self.pedidos:
            if pedido.id == id:
                pedido.statusUpdate()
                return f"Pedido {id} atualizado para {pedido.status}"
        return "Número do pedido incorreto."

    def listOrders(self):
        """Lista todos os pedidos do dia."""
        return [pedido.orderStatus() for pedido in self.pedidos]
    
    def listPendingOrders(self):
        """Lista todos os pedidos pendentes."""
        return [pedido.orderStatus() for pedido in self.pedidos if pedido.status != "Entregue"]
    
    def dailyRevenue(self):
        return sum(pedido.valor_total for pedido in self.pedidos if pedido.status == "Entregue")


