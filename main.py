from restaurante import Restaurate
from menu import MENU

# Criando instância do restaurante
restaurante = Restaurate()

# Criando um dicionário {id: (nome, preço)} para facilitar a busca
PRECOS_PRATOS = {item["id"]: (item["nome"], item["preco"]) for item in MENU}

def main():
    while True:
        print("Menu Principal:")
        print("1 Adicionar Pedido")
        print("2 Atualizar Status do Pedido")
        print("3 Listar Todos os Pedidos")
        print("4 Listar Pedidos Pendentes")
        print("5 Mostrar Receita do Dia")
        print("6 Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            nome_cliente = input("\nNome do Cliente: ").strip()
            codigos = input("Digite os códigos dos itens separados por vírgula: ").strip().split(",")

            itens_pedido = []
            for cod in codigos:
                try:
                    cod = int(cod.strip())  # Converte para inteiro
                    if cod in PRECOS_PRATOS:
                        itens_pedido.append({"nome": PRECOS_PRATOS[cod][0], "preco": PRECOS_PRATOS[cod][1]})
                    else:
                        print(f"Código {cod} não encontrado no menu.")
                except ValueError:
                    print(f"Entrada inválida: {cod} não é um número.")

            if itens_pedido:
                id_pedido = restaurante.makeOrder(nome_cliente, itens_pedido)
                print(f"Pedido {id_pedido} para {nome_cliente} adicionado com sucesso!")

        elif opcao == "2":
            id_pedido = input("\nID do Pedido a ser atualizado: ").strip()
            print(restaurante.statusUpdate(id_pedido))

        elif opcao == "3":
            print("\nTodos os Pedidos:")
            pedidos = restaurante.listOrders()
            for pedido in pedidos:
                print(pedido)

        elif opcao == "4":
            print("\nPedidos Pendentes:")
            pedidos_pendentes = restaurante.listPendingOrders()
            for pedido in pedidos_pendentes:
                print(pedido)

        elif opcao == "5":
            print(f"\nReceita do Dia: R$ {restaurante.dailyRevenue():.2f}")

        elif opcao == "6":
            print("\nEncerrando o sistema. Até mais!")
            break

        else:
            print("Opção inválida. Escolha um número de 1 a 6.")

if __name__ == "__main__":
    main()
