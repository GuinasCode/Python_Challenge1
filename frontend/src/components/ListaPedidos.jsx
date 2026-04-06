export default function ListaPedidos({ pedidos = [], onEntregar }) {
  return (
    <div>
      <h2>Pedidos</h2>
      {pedidos.map((p) => (
        <div key={p.id} style={{ border: '1px solid #ddd', marginBottom: 8, padding: 8 }}>
          <strong>#{p.id}</strong> - {p.nome_cliente} - {p.status} - R$ {Number(p.valor_total).toFixed(2)}
          <div>{p.itens}</div>
          {p.status === 'Pronto' && <button onClick={() => onEntregar(p.id)}>Marcar como Entregue</button>}
        </div>
      ))}
    </div>
  )
}
