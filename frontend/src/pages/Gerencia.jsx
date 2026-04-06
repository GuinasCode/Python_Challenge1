import { useEffect, useMemo, useState } from 'react'
import Dashboard from '../components/Dashboard'
import {
  atualizarCategoria,
  atualizarItem,
  criarCategoria,
  criarItem,
  listarCategorias,
  listarMenu,
  listarPedidos,
  listarPendentes,
  receita,
  removerCategoria,
  removerItem,
} from '../services/api'

function readFileAsDataUrl(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => resolve(reader.result)
    reader.onerror = reject
    reader.readAsDataURL(file)
  })
}

const initialItemForm = {
  id: null,
  item: '',
  valor: '',
  categoria_id: '',
  imagem_base64: '',
}

const initialCategoryForm = {
  id: null,
  nome: '',
  ordem: 10,
}

export default function Gerencia() {
  const [stats, setStats] = useState({ receitaHoje: 0, totalPedidos: 0, pendentes: 0 })
  const [menu, setMenu] = useState([])
  const [categorias, setCategorias] = useState([])
  const [itemForm, setItemForm] = useState(initialItemForm)
  const [categoryForm, setCategoryForm] = useState(initialCategoryForm)
  const [loading, setLoading] = useState(true)
  const [savingItem, setSavingItem] = useState(false)
  const [savingCategory, setSavingCategory] = useState(false)

  const load = async () => {
    try {
      const [r, p, pend, m, c] = await Promise.all([
        receita(),
        listarPedidos(),
        listarPendentes(),
        listarMenu(),
        listarCategorias(),
      ])
      setStats({ receitaHoje: r.data.total, totalPedidos: p.data.length, pendentes: pend.data.length })
      setMenu(m.data)
      setCategorias(c.data)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    load()
  }, [])

  const groupedMenu = useMemo(() => categorias.map((categoria) => ({
    ...categoria,
    itens: menu.filter((item) => item.categoria_id === categoria.id),
  })), [categorias, menu])

  const submitCategory = async (event) => {
    event.preventDefault()
    try {
      setSavingCategory(true)
      const payload = {
        nome: categoryForm.nome.trim(),
        ordem: Number(categoryForm.ordem || 0),
      }
      if (!payload.nome) {
        alert('Informe o nome da categoria.')
        return
      }

      if (categoryForm.id) await atualizarCategoria(categoryForm.id, payload)
      else await criarCategoria(payload)

      setCategoryForm(initialCategoryForm)
      await load()
    } catch (error) {
      alert(error.response?.data?.detail || 'Não foi possível salvar a categoria.')
    } finally {
      setSavingCategory(false)
    }
  }

  const submitItem = async (event) => {
    event.preventDefault()
    try {
      setSavingItem(true)
      if (!itemForm.categoria_id) {
        alert('Selecione uma categoria para o item.')
        return
      }
      const payload = {
        item: itemForm.item.trim(),
        valor: Number(itemForm.valor),
        categoria_id: Number(itemForm.categoria_id),
        imagem_base64: itemForm.imagem_base64 || null,
      }
      if (!payload.item || !payload.valor) {
        alert('Preencha nome e valor do item.')
        return
      }

      if (itemForm.id) await atualizarItem(itemForm.id, payload)
      else await criarItem(payload)

      setItemForm(initialItemForm)
      await load()
    } catch (error) {
      alert(error.response?.data?.detail || 'Não foi possível salvar o item.')
    } finally {
      setSavingItem(false)
    }
  }

  const handleImageChange = async (event) => {
    const file = event.target.files?.[0]
    if (!file) return
    const image = await readFileAsDataUrl(file)
    setItemForm((prev) => ({ ...prev, imagem_base64: image }))
  }

  if (loading) {
    return <div className="page-shell"><div className="surface">Carregando painel gerencial...</div></div>
  }

  return (
    <section className="page-shell page-shell--stacked">
      <div className="surface">
        <Dashboard {...stats} />
      </div>

      <div className="management-grid">
        <section className="surface">
          <div className="section-header section-header--compact">
            <div>
              <p className="eyebrow">Categorias</p>
              <h2>Gerenciar seções do cardápio</h2>
            </div>
          </div>

          <form className="form-grid" onSubmit={submitCategory}>
            <label className="field">
              <span>Nome da categoria</span>
              <input
                value={categoryForm.nome}
                onChange={(event) => setCategoryForm((prev) => ({ ...prev, nome: event.target.value }))}
                placeholder="Ex.: Entradas"
              />
            </label>
            <label className="field">
              <span>Ordem</span>
              <input
                type="number"
                min="0"
                value={categoryForm.ordem}
                onChange={(event) => setCategoryForm((prev) => ({ ...prev, ordem: event.target.value }))}
              />
            </label>
            <div className="form-actions form-actions--full">
              <button type="submit" className="primary-button" disabled={savingCategory}>
                {savingCategory ? 'Salvando...' : (categoryForm.id ? 'Atualizar categoria' : 'Criar categoria')}
              </button>
              <button type="button" className="ghost-button" onClick={() => setCategoryForm(initialCategoryForm)}>
                Limpar
              </button>
            </div>
          </form>

          <div className="stack-list">
            {categorias.map((categoria) => (
              <div key={categoria.id} className="stack-list__item">
                <div>
                  <strong>{categoria.nome}</strong>
                  <span>Ordem: {categoria.ordem} · {categoria.total_itens} item(ns)</span>
                </div>
                <div className="inline-actions">
                  <button type="button" className="ghost-button" onClick={() => setCategoryForm(categoria)}>Editar</button>
                  <button
                    type="button"
                    className="ghost-button ghost-button--danger"
                    onClick={async () => {
                      if (!window.confirm(`Excluir a categoria ${categoria.nome}?`)) return
                      try {
                        await removerCategoria(categoria.id)
                        await load()
                      } catch (error) {
                        alert(error.response?.data?.detail || 'Não foi possível excluir a categoria.')
                      }
                    }}
                  >
                    Excluir
                  </button>
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="surface">
          <div className="section-header section-header--compact">
            <div>
              <p className="eyebrow">Cardápio</p>
              <h2>Cadastrar itens com foto</h2>
            </div>
          </div>

          <form className="form-grid" onSubmit={submitItem}>
            <label className="field field--full">
              <span>Nome do item</span>
              <input
                value={itemForm.item}
                onChange={(event) => setItemForm((prev) => ({ ...prev, item: event.target.value }))}
                placeholder="Ex.: Hambúrguer artesanal"
              />
            </label>

            <label className="field">
              <span>Valor</span>
              <input
                type="number"
                min="0"
                step="0.01"
                value={itemForm.valor}
                onChange={(event) => setItemForm((prev) => ({ ...prev, valor: event.target.value }))}
              />
            </label>

            <label className="field">
              <span>Categoria</span>
              <select
                value={itemForm.categoria_id}
                onChange={(event) => setItemForm((prev) => ({ ...prev, categoria_id: event.target.value }))}
              >
                <option value="">Selecione...</option>
                {categorias.map((categoria) => (
                  <option key={categoria.id} value={categoria.id}>{categoria.nome}</option>
                ))}
              </select>
            </label>

            <label className="field field--full">
              <span>Imagem do produto</span>
              <input type="file" accept="image/*" onChange={handleImageChange} />
            </label>

            {itemForm.imagem_base64 && (
              <div className="image-preview field--full">
                <img src={itemForm.imagem_base64} alt="Prévia do item" />
                <button type="button" className="ghost-button" onClick={() => setItemForm((prev) => ({ ...prev, imagem_base64: '' }))}>
                  Remover imagem
                </button>
              </div>
            )}

            <div className="form-actions form-actions--full">
              <button type="submit" className="primary-button" disabled={savingItem}>
                {savingItem ? 'Salvando...' : (itemForm.id ? 'Atualizar item' : 'Criar item')}
              </button>
              <button type="button" className="ghost-button" onClick={() => setItemForm(initialItemForm)}>
                Limpar
              </button>
            </div>
          </form>
        </section>
      </div>

      <section className="surface">
        <div className="section-header section-header--compact">
          <div>
            <p className="eyebrow">Itens por categoria</p>
            <h2>Visualização do cardápio</h2>
          </div>
        </div>

        <div className="menu-sections">
          {groupedMenu.map((categoria) => (
            <section key={categoria.id} className="category-section">
              <div className="section-header section-header--compact">
                <div>
                  <p className="eyebrow">{categoria.total_itens} item(ns)</p>
                  <h3>{categoria.nome}</h3>
                </div>
                <span className="pill">Ordem {categoria.ordem}</span>
              </div>

              <div className="menu-grid">
                {categoria.itens.map((item) => (
                  <article key={item.id} className="menu-card menu-card--compact">
                    <img className="menu-card__image" src={item.imagem_base64} alt={item.item} />
                    <div className="menu-card__content">
                      <div>
                        <p className="menu-card__category">{item.categoria_nome}</p>
                        <h4>{item.item}</h4>
                        <p className="menu-card__price">R$ {Number(item.valor).toFixed(2)}</p>
                      </div>
                      <div className="inline-actions inline-actions--stacked">
                        <button
                          type="button"
                          className="ghost-button"
                          onClick={() => setItemForm({
                            id: item.id,
                            item: item.item,
                            valor: item.valor,
                            categoria_id: item.categoria_id,
                            imagem_base64: item.imagem_base64,
                          })}
                        >
                          Editar
                        </button>
                        <button
                          type="button"
                          className="ghost-button ghost-button--danger"
                          onClick={async () => {
                            if (!window.confirm(`Excluir ${item.item}?`)) return
                            await removerItem(item.id)
                            await load()
                          }}
                        >
                          Excluir
                        </button>
                      </div>
                    </div>
                  </article>
                ))}
              </div>
            </section>
          ))}
        </div>
      </section>
    </section>
  )
}
