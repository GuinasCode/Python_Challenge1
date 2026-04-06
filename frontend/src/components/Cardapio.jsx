function groupMenu(menu = []) {
  const groups = new Map()

  menu.forEach((item) => {
    const key = item.categoria_id || `sem-categoria-${item.categoria_nome || 'Sem categoria'}`
    if (!groups.has(key)) {
      groups.set(key, {
        categoriaId: item.categoria_id,
        categoriaNome: item.categoria_nome || 'Sem categoria',
        categoriaOrdem: item.categoria_ordem ?? 999,
        itens: [],
      })
    }
    groups.get(key).itens.push(item)
  })

  return Array.from(groups.values())
    .sort((a, b) => (a.categoriaOrdem - b.categoriaOrdem) || a.categoriaNome.localeCompare(b.categoriaNome))
    .map((group) => ({
      ...group,
      itens: [...group.itens].sort((a, b) => a.item.localeCompare(b.item)),
    }))
}

export default function Cardapio({ menu = [], quantidades = {}, onIncrement, onDecrement }) {
  const groupedMenu = groupMenu(menu)

  return (
    <div className="menu-sections">
      {groupedMenu.map((group) => (
        <section key={group.categoriaNome} className="category-section">
          <div className="section-header">
            <div>
              <p className="eyebrow">Categoria</p>
              <h3>{group.categoriaNome}</h3>
            </div>
            <span className="pill">{group.itens.length} item(ns)</span>
          </div>

          <div className="menu-grid">
            {group.itens.map((item) => {
              const quantidade = quantidades[item.id] || 0
              return (
                <article key={item.id} className="menu-card">
                  <img className="menu-card__image" src={item.imagem_base64} alt={item.item} />
                  <div className="menu-card__content">
                    <div>
                      <p className="menu-card__category">{group.categoriaNome}</p>
                      <h4>{item.item}</h4>
                      <p className="menu-card__price">R$ {Number(item.valor).toFixed(2)}</p>
                    </div>
                    <div className="quantity-stepper">
                      <button type="button" onClick={() => onDecrement(item.id)} disabled={quantidade === 0}>-</button>
                      <span>{quantidade}</span>
                      <button type="button" onClick={() => onIncrement(item.id)}>+</button>
                    </div>
                  </div>
                </article>
              )
            })}
          </div>
        </section>
      ))}
    </div>
  )
}
