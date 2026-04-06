export default function PainelCozinha({ pedidos = [], onAvancar }) {
  return (
    <div>
      <h2>Painel da Cozinha</h2>
      {pedidos
        .filter((p) => p.status === 'Pendente' || p.status === 'Em preparo')
        .map((p) => (
          <div key={p.id} style={{ marginBottom: 8, padding: 8, background: p.status === 'Pendente' ? '#FEE2E2' : '#FEF3C7' }}>
            #{p.id} - {p.nome_cliente} - {p.status}
            <button onClick={() => onAvancar(p.id)} style={{ marginLeft: 8 }}>
              {p.status === 'Pendente' ? 'Iniciar Preparo' : 'Marcar como Pronto'}
            </button>
          </div>
        ))}
    </div>
  )
}
