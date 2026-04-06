import { useEffect, useState } from 'react'
import Dashboard from '../components/Dashboard'
import { atualizarItem, criarItem, listarMenu, listarPedidos, listarPendentes, receita, removerItem } from '../services/api'

export default function Gerencia() {
  const [stats, setStats] = useState({ receitaHoje: 0, totalPedidos: 0, pendentes: 0 })
  const [menu, setMenu] = useState([])

  const load = async () => {
    const [r, p, pend, m] = await Promise.all([receita(), listarPedidos(), listarPendentes(), listarMenu()])
    setStats({ receitaHoje: r.data.total, totalPedidos: p.data.length, pendentes: pend.data.length })
    setMenu(m.data)
  }

  useEffect(() => {
    load()
  }, [])

  return (
    <div>
      <Dashboard {...stats} />
      <h3>Gestão do Cardápio</h3>
      <button onClick={async () => { await criarItem({ item: 'Novo Item', valor: 10 }); load() }}>Adicionar Item</button>
      {menu.map((item) => (
        <div key={item.id}>
          {item.item} - R$ {Number(item.valor).toFixed(2)}
          <button onClick={async () => { await atualizarItem(item.id, { item: item.item + ' *', valor: item.valor }); load() }}>Editar</button>
          <button onClick={async () => { if (confirm('Excluir item?')) { await removerItem(item.id); load() } }}>Excluir</button>
        </div>
      ))}
    </div>
  )
}
