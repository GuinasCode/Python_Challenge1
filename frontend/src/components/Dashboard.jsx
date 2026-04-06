export default function Dashboard({ receitaHoje, totalPedidos, pendentes }) {
  const cards = [
    { label: 'Receita do dia', value: `R$ ${Number(receitaHoje || 0).toFixed(2)}` },
    { label: 'Pedidos do dia', value: totalPedidos },
    { label: 'Pedidos pendentes', value: pendentes },
  ]

  return (
    <div>
      <p className="eyebrow">Gerência</p>
      <h1>Painel gerencial</h1>
      <div className="dashboard-grid">
        {cards.map((card) => (
          <div key={card.label} className="dashboard-card">
            <span>{card.label}</span>
            <strong>{card.value}</strong>
          </div>
        ))}
      </div>
    </div>
  )
}
