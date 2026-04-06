import { useEffect, useState } from 'react'
import ListaPedidos from '../components/ListaPedidos'
import NovoPedido from '../components/NovoPedido'
import { avancarStatus, criarPedido, listarMenu, listarPedidos } from '../services/api'

export default function Garcom() {
  const [menu, setMenu] = useState([])
  const [pedidos, setPedidos] = useState([])

  const carregar = async () => {
    const [m, p] = await Promise.all([listarMenu(), listarPedidos()])
    setMenu(m.data)
    setPedidos(p.data)
  }

  useEffect(() => {
    carregar()
  }, [])

  return (
    <div>
      <NovoPedido
        menu={menu}
        onSubmit={async (payload) => {
          const resp = await criarPedido(payload)
          alert(`Pedido ${resp.data.id} criado com sucesso`)
          carregar()
        }}
      />
      <ListaPedidos
        pedidos={pedidos}
        onEntregar={async (id) => {
          await avancarStatus(id)
          carregar()
        }}
      />
    </div>
  )
}
