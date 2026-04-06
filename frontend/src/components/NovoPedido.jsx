import { useState } from 'react'
import Cardapio from './Cardapio'

export default function NovoPedido({ menu, onSubmit }) {
  const [nomeCliente, setNomeCliente] = useState('')
  const [itens, setItens] = useState([])

  const toggleItem = (id) => {
    setItens((prev) => (prev.includes(id) ? prev.filter((i) => i !== id) : [...prev, id]))
  }

  return (
    <div>
      <h2>Novo Pedido</h2>
      <input placeholder="Nome do cliente" value={nomeCliente} onChange={(e) => setNomeCliente(e.target.value)} />
      <Cardapio menu={menu} selecionados={itens} onToggle={toggleItem} />
      <button onClick={() => onSubmit({ nome_cliente: nomeCliente, itens })}>Fazer Pedido</button>
    </div>
  )
}
