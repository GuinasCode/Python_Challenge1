from restaurante import Restaurante

restaurante = Restaurante()

def main():
    while True:
        print("\nMenu Principal:\n")
        print("0 Listar Cardápio")
        print("1 Adicionar Pedido")
        print("2 Verificar Pedido")
        print("3 Atualizar Status do Pedido") 
        print("4 Listar Pedidos")
        print("5 Listar Pedidos Pendentes")
        print("6 Mostrar Receita")
        print("7 Sair")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "0":
            menu = restaurante.getMenu()            
            if menu:
                print("\n🍽️  Cardápio do Restaurante 🍽️")
                print("-" * 55)
                print(f"{'ID':<5} {'Item':<35} {'Preço':>10}")
                print("-" * 55)
        
                for item in menu:
                    item_id, nome, preco = item
                    print(f"{item_id:<5} {nome:<35} R$ {preco:>7.2f}")
                print("-" * 55)        
        
        elif opcao == "1":
            nome_cliente = input("\nNome do Cliente: ").strip()
            codigos = input("Digite os códigos dos itens separados por vírgula: ").strip().split(",")

            mensagem = restaurante.makeOrder(nome_cliente, codigos)
            if mensagem:
                print(mensagem)
            else:
                print("Erro ao criar o pedido.")

        elif opcao == "2":
            pedido = input("\nInforme o id do pedido: ")
            status_pedido = restaurante.checkOrderStatus(pedido)
            print(status_pedido)

        elif opcao == "3":
            id_pedido = input("\nID do Pedido a ser atualizado: ").strip()
            print(restaurante.statusUpdate(id_pedido))

        elif opcao == "4":
            print("\nEscolha\n"
                    "1 - Para mostrar os pedidos de hoje\n"
                    "2 - Para mostrar os pedidos de uma outra data\n"
                    "3 - Para mostrar todos os pedidos registrados\n")
            sub_opcao = input("\nEscolha:")

            if sub_opcao == "1":
                pedidos = restaurante.listOrders()
                print(pedidos)
            
            elif sub_opcao == "2":
                data_input = input("Digite a data que deseja consultar no formato DD/MM/AAAA: ")
                pedidos = restaurante.listOrders(data_input)
                print(pedidos)
            
            elif sub_opcao == "3":
                pedidos = restaurante.listAllOrders()
                print(pedidos)

        elif opcao == "5":
            pedidos = restaurante.listPendingOrders()
            print(pedidos)

        elif opcao == "6":
            print("\nEscolha:\n"
                   "1 - Para mostrar a receita de hoje.\n"
                   "2 - Para mostrar a receiota de um dia específico.\n"
                   "3 - Para mostrar a de um intervalo de datas específico.\n")
            sub_opcao = input("\nEscolha:")

            if sub_opcao == "1":
                revenue = restaurante.getRevenue()
                print(revenue)
            
            elif sub_opcao == "2":
                print("\nA datas devem ser preenchidas no formato DD/MM/AAAA.")
                data_input = input("Digite a data que deseja consultar: ")
                revenue = restaurante.getRevenue(data_input)
                print(revenue)
            
            elif sub_opcao == "3":
                print("\nTodas as datas devem ser preenchidas no formato DD/MM/AAAA.")
                inicio = input("Digite a data inicial: ")
                fim = input("Digite a data final: ")
                revenue = restaurante.getRevenue(inicio, fim)
                print(revenue)

        elif opcao == "7":
            print("\nEncerrando o sistema. Até mais!")
            break

        else:
            print("Opção inválida. Escolha um número de 0 a 6.")

if __name__ == "__main__":
    main()