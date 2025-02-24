
from datetime import datetime

status = ["Pendente","Em prepapro", "Pronto","Entregue"]

class idGenerator:
        idPedido = {}
    
        @classmethod    
        def gerarId(cls):
            data_atual = datetime.now().strftime("%y%m%d")
            cls.idPedido[data_atual] = cls.idPedido.get(data_atual, 0) + 1
        
            indice = f"{cls.idPedido[data_atual]:02d}"
            return f"{data_atual}{indice}"
