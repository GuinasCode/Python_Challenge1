export default function Dashboard({ receitaHoje, totalPedidos, pendentes }) {
  return (
    <div>
      <h2>Dashboard Gerencial</h2>
      <div>Receita de hoje: R$ {Number(receitaHoje || 0).toFixed(2)}</div>
      <div>Pedidos do dia: {totalPedidos}</div>
      <div>Pedidos pendentes: {pendentes}</div>
    </div>
  )
}
