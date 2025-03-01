from utils import idGenerator, status
from utils import DatabaseManager

class Order:
    idGenerator()
              
    def __init__(self, cliente, itens):      
        self.id = idGenerator.gerarId()
        self.client = cliente
        self.itens = itens
        self.index = 0
        self.status = status[self.index]
        self.valor_total = sum(item["preco"] for item in self.itens)

    @staticmethod
    def getMenu():
        with DatabaseManager() as db: 
            menu = db.execute_query('''SELECT * FROM menu;''')
            return menu
   
    def statusUpdate(self):
        if self.status != "Entregue":
            self.index += 1
            self.status = status[self.index]

    def orderStatus(self):
        itens_lista = [item["nome"] for item in self.itens]
        return f"Pedido {self.id} | Cliente: {self.client} | Status: {self.status} | Itens: {', '.join(itens_lista)} | Total: R$ {self.valor_total:.2f}"
    
""" if __name__ == "__main__":
        menu = getMenu.__func__()
        if menu:
            print("\n🍽️  Cardápio do Restaurante 🍽️")
            print("-" * 55)
            print(f"{'ID':<5} {'Item':<35} {'Preço':>10}")
            print("-" * 55)
        
            for item in menu:
                item_id, nome, preco = item
                print(f"{item_id:<5} {nome:<35} R$ {preco:>7.2f}")
            print("-" * 55)          """