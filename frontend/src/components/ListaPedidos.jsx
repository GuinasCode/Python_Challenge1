const STATUS_THEME = {
  Pendente: 'status status--danger',
  'Em preparo': 'status status--warning',
  Pronto: 'status status--success',
  Entregue: 'status status--muted',
}

export default function ListaPedidos({ pedidos = [], onEntregar }) {
  return (
    <section className="surface">
      <div className="section-header section-header--compact">
        <div>
          <p className="eyebrow">Acompanhamento</p>
          <h2>Pedidos lançados</h2>
        </div>
        <span className="pill">{pedidos.length} pedido(s)</span>
      </div>

      <div className="orders-list">
        {pedidos.length === 0 && (
          <div className="empty-state">
            <p>Nenhum pedido encontrado.</p>
            <span>Os pedidos criados aparecerão aqui para acompanhamento.</span>
          </div>
        )}

        {pedidos.map((pedido) => (
          <article key={pedido.id} className="order-card">
            <div className="order-card__header">
              <div>
                <p className="eyebrow">Pedido #{pedido.id}</p>
                <h3>{pedido.nome_cliente}</h3>
              </div>
              <div className="order-card__meta">
                <span className={STATUS_THEME[pedido.status] || 'status'}>{pedido.status}</span>
                <strong>R$ {Number(pedido.valor_total).toFixed(2)}</strong>
              </div>
            </div>

            <div className="order-item-list">
              {(pedido.itens_detalhados || []).map((item, index) => (
                <div key={`${pedido.id}-${item.item_id || index}`} className="order-item-row">
                  <img src={item.imagem_base64} alt={item.nome} className="order-item-row__image" />
                  <div>
                    <strong>{item.nome}</strong>
                    <span>{item.categoria_nome}</span>
                  </div>
                  <span>{item.quantidade}x</span>
                  <strong>R$ {Number(item.subtotal).toFixed(2)}</strong>
                </div>
              ))}
            </div>

            {pedido.status === 'Pronto' && (
              <button type="button" className="secondary-button" onClick={() => onEntregar(pedido.id)}>
                Marcar como entregue
              </button>
            )}
          </article>
        ))}
      </div>
    </section>
  )
}
