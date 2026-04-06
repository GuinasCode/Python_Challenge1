export default function Cardapio({ menu = [], selecionados = [], onToggle }) {
  return (
    <div>
      <h3>Cardápio</h3>
      {menu.map((item) => (
        <label key={item.id} style={{ display: 'block' }}>
          <input
            type="checkbox"
            checked={selecionados.includes(item.id)}
            onChange={() => onToggle(item.id)}
          />
          {item.item} - R$ {Number(item.valor).toFixed(2)}
        </label>
      ))}
    </div>
  )
}
