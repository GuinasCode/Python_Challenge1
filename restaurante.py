from pedido import Order

class Restaurante:
    def __init__(self):
        self.pedidos = []
       
    def getMenu(self):
        menu = Order.getMenu()
        return menu
    
    def makeOrder(self, cliente, itens):
        order = Order(cliente=cliente, itens=itens, status="Pendente")
        return order.new_order()
    
    def checkOrderStatus(self, id):
        order = Order.check_order(id)
        return f"O pedido {id} atualmente está: {order}"
    
    def statusUpdate(self, id):
        return Order.update_status(id)
    
    def listOrders(self, date=None):
        return Order.list_orders(date)
    
    def listAllOrders(self):
        return Order.list_all_orders()
  
    def listPendingOrders(self):
        return Order.list_pending_orders()
    
    def getRevenue(self, start_date=None, end_date=None):
        return Order.get_revenue(start_date, end_date)