# Define a classe Pedido
from utils import idGenerator, status

class Order:
    idGenerator()
              
    def __init__(self, cliente, itens):      
        self.id = idGenerator.gerarId()
        self.client = cliente
        self.itens = itens
        self.index = 0
        self.status = status[self.index]
        self.valor_total = sum(item["preco"] for item in self.itens)
   
    def statusUpdate(self):
        """Atualiza o status do pedido automaticamente."""
        if self.status != "Entregue":
            self.index += 1
            self.status = status[self.index]  # Atualiza o status

    def orderStatus(self):
        """Retorna o status atual do pedido."""
        itens_lista = [item["nome"] for item in self.itens]  # Ajuste para extrair o nome dos itens
        return f"Pedido {self.id} | Cliente: {self.client} | Status: {self.status} | Itens: {', '.join(itens_lista)} | Total: R$ {self.valor_total:.2f}"
