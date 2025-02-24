from menu import MENU
from pedido import Order

class Restaurate:
    def __init__(self):
        self.pedidos = []
    
    def makeOrder(self, cliente, itens):
        pedido = Order(cliente, itens)
        self.pedidos.append(pedido)
        return pedido.id
    
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


