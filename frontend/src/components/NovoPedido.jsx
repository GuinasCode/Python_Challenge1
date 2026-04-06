import { useMemo, useState } from 'react'
import Cardapio from './Cardapio'

export default function NovoPedido({ menu, onSubmit }) {
  const [nomeCliente, setNomeCliente] = useState('')
  const [quantidades, setQuantidades] = useState({})
  const [submitting, setSubmitting] = useState(false)

  const itensSelecionados = useMemo(
    () => menu
      .filter((item) => (quantidades[item.id] || 0) > 0)
      .map((item) => ({
        ...item,
        quantidade: quantidades[item.id],
        subtotal: Number(item.valor) * quantidades[item.id],
      })),
    [menu, quantidades],
  )

  const total = itensSelecionados.reduce((acc, item) => acc + item.subtotal, 0)

  const alterarQuantidade = (itemId, delta) => {
    setQuantidades((prev) => {
      const nextQuantity = Math.max(0, (prev[itemId] || 0) + delta)
      if (nextQuantity === 0) {
        const { [itemId]: _, ...rest } = prev
        return rest
      }
      return { ...prev, [itemId]: nextQuantity }
    })
  }

  const handleSubmit = async () => {
    if (!nomeCliente.trim()) {
      alert('Informe o nome do cliente.')
      return
    }
    if (itensSelecionados.length === 0) {
      alert('Adicione ao menos um item ao pedido.')
      return
    }

    try {
      setSubmitting(true)
      await onSubmit({
        nome_cliente: nomeCliente.trim(),
        itens: itensSelecionados.map((item) => ({ item_id: item.id, quantidade: item.quantidade })),
      })
      setNomeCliente('')
      setQuantidades({})
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <section className="page-shell waiter-layout">
      <div className="surface hero-panel">
        <div>
          <p className="eyebrow">Garçom</p>
          <h1>Registro de pedidos com fotos, categorias e quantidades</h1>
          <p className="hero-copy">
            Organize a tomada de pedidos por categoria, ajuste quantidades rapidamente e confirme o total antes de enviar para a cozinha.
          </p>
        </div>
        <div className="hero-panel__meta">
          <label className="field">
            <span>Cliente</span>
            <input
              placeholder="Ex.: Mesa 12 / João"
              value={nomeCliente}
              onChange={(event) => setNomeCliente(event.target.value)}
            />
          </label>
          <div className="summary-kpis">
            <div>
              <strong>{itensSelecionados.length}</strong>
              <span>itens distintos</span>
            </div>
            <div>
              <strong>{Object.values(quantidades).reduce((acc, value) => acc + value, 0)}</strong>
              <span>unidades</span>
            </div>
            <div>
              <strong>R$ {total.toFixed(2)}</strong>
              <span>total</span>
            </div>
          </div>
        </div>
      </div>

      <div className="waiter-columns">
        <div className="surface">
          <div className="section-header section-header--compact">
            <div>
              <p className="eyebrow">Cardápio</p>
              <h2>Escolha os itens por categoria</h2>
            </div>
          </div>
          <Cardapio
            menu={menu}
            quantidades={quantidades}
            onIncrement={(id) => alterarQuantidade(id, 1)}
            onDecrement={(id) => alterarQuantidade(id, -1)}
          />
        </div>

        <aside className="surface order-summary">
          <div className="section-header section-header--compact">
            <div>
              <p className="eyebrow">Pedido atual</p>
              <h2>Resumo visual do pedido</h2>
            </div>
          </div>

          {itensSelecionados.length === 0 ? (
            <div className="empty-state">
              <p>Nenhum item selecionado ainda.</p>
              <span>Adicione produtos no cardápio para montar o pedido.</span>
            </div>
          ) : (
            <div className="order-summary__items">
              {itensSelecionados.map((item) => (
                <div key={item.id} className="summary-item">
                  <img src={item.imagem_base64} alt={item.item} className="summary-item__image" />
                  <div className="summary-item__content">
                    <strong>{item.item}</strong>
                    <span>{item.categoria_nome || 'Sem categoria'}</span>
                    <small>{item.quantidade}x de R$ {Number(item.valor).toFixed(2)}</small>
                  </div>
                  <div className="summary-item__actions">
                    <button type="button" onClick={() => alterarQuantidade(item.id, -1)}>-</button>
                    <span>{item.quantidade}</span>
                    <button type="button" onClick={() => alterarQuantidade(item.id, 1)}>+</button>
                  </div>
                  <strong className="summary-item__subtotal">R$ {item.subtotal.toFixed(2)}</strong>
                </div>
              ))}
            </div>
          )}

          <div className="order-summary__footer">
            <div>
              <span>Total do pedido</span>
              <strong>R$ {total.toFixed(2)}</strong>
            </div>
            <button type="button" className="primary-button" onClick={handleSubmit} disabled={submitting}>
              {submitting ? 'Enviando...' : 'Enviar pedido'}
            </button>
          </div>
        </aside>
      </div>
    </section>
  )
}
