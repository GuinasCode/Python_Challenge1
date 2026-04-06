import { useEffect, useState } from 'react'
import ListaPedidos from '../components/ListaPedidos'
import NovoPedido from '../components/NovoPedido'
import { avancarStatus, criarPedido, listarMenu, listarPedidos } from '../services/api'

export default function Garcom() {
  const [menu, setMenu] = useState([])
  const [pedidos, setPedidos] = useState([])
  const [loading, setLoading] = useState(true)

  const carregar = async () => {
    try {
      const [m, p] = await Promise.all([listarMenu(), listarPedidos()])
      setMenu(m.data)
      setPedidos(p.data)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    carregar()
  }, [])

  if (loading) {
    return <div className="page-shell"><div className="surface">Carregando ambiente do garçom...</div></div>
  }

  return (
    <div className="page-shell page-shell--stacked">
      <NovoPedido
        menu={menu}
        onSubmit={async (payload) => {
          const resp = await criarPedido(payload)
          alert(`Pedido ${resp.data.id} criado com sucesso`)
          await carregar()
        }}
      />
      <ListaPedidos
        pedidos={pedidos}
        onEntregar={async (id) => {
          await avancarStatus(id)
          await carregar()
        }}
      />
    </div>
  )
}
