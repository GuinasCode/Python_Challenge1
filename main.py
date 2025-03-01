from restaurante import Restaurate

restaurante = Restaurate()

def main():
    while True:
        print("Menu Principal:")
        print("0 Listar Cardápio")
        print("1 Adicionar Pedido")
        print("2 Atualizar Status do Pedido") 
        print("3 Listar Pedidos")
        print("4 Listar Pedidos Pendentes")
        print("5 Mostrar Receita do Dia")
        print("6 Sair")

        opcao = input("Escolha uma opção: ").strip()

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
            id_pedido = input("\nID do Pedido a ser atualizado: ").strip()
            print(restaurante.statusUpdate(id_pedido))

        elif opcao == "3":
            sub_opcao = input("\nEscolha:\n"
                              "1 - Para mostrar os pedidos de hoje\n"
                              "2 - Para mostrar os pedidos de uma outra data\n"
                              "3 - Para mostrar todos os pedidos registrados\n")
            
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
            print("Opção inválida. Escolha um número de 0 a 6.")

if __name__ == "__main__":
    main()