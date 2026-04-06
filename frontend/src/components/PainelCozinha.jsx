export default function PainelCozinha({ pedidos = [], onAvancar }) {
  const ativos = pedidos.filter((pedido) => pedido.status === 'Pendente' || pedido.status === 'Em preparo')

  return (
    <section className="page-shell">
      <div className="surface">
        <div className="section-header">
          <div>
            <p className="eyebrow">Cozinha</p>
            <h1>Painel operacional</h1>
          </div>
          <span className="pill">{ativos.length} pedido(s) ativos</span>
        </div>

        <div className="orders-list">
          {ativos.length === 0 && (
            <div className="empty-state">
              <p>Nenhum pedido aguardando preparo.</p>
              <span>Os novos pedidos aparecerão aqui automaticamente.</span>
            </div>
          )}

          {ativos.map((pedido) => (
            <article key={pedido.id} className="order-card order-card--kitchen">
              <div className="order-card__header">
                <div>
                  <p className="eyebrow">Pedido #{pedido.id}</p>
                  <h3>{pedido.nome_cliente}</h3>
                </div>
                <span className={`status ${pedido.status === 'Pendente' ? 'status--danger' : 'status--warning'}`}>{pedido.status}</span>
              </div>

              <div className="order-item-list">
                {(pedido.itens_detalhados || []).map((item, index) => (
                  <div key={`${pedido.id}-${item.item_id || index}`} className="kitchen-item-row">
                    <span>{item.quantidade}x</span>
                    <strong>{item.nome}</strong>
                    <small>{item.categoria_nome}</small>
                  </div>
                ))}
              </div>

              <button type="button" className="primary-button" onClick={() => onAvancar(pedido.id)}>
                {pedido.status === 'Pendente' ? 'Iniciar preparo' : 'Marcar como pronto'}
              </button>
            </article>
          ))}
        </div>
      </div>
    </section>
  )
}
