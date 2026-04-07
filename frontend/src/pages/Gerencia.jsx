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

function normalizeItemForm(item = initialItemForm) {
  return {
    id: item.id ?? null,
    item: item.item ?? '',
    valor: item.valor != null ? String(item.valor) : '',
    categoria_id: item.categoria_id != null ? String(item.categoria_id) : '',
    imagem_base64: item.imagem_base64 || '',
  }
}

export default function Gerencia() {
  const [stats, setStats] = useState({ receitaHoje: 0, totalPedidos: 0, pendentes: 0 })
  const [menu, setMenu] = useState([])
  const [categorias, setCategorias] = useState([])
  const [itemForm, setItemForm] = useState(initialItemForm)
  const [editItemForm, setEditItemForm] = useState(null)
  const [categoryForm, setCategoryForm] = useState(initialCategoryForm)
  const [loading, setLoading] = useState(true)
  const [savingItem, setSavingItem] = useState(false)
  const [savingEditItem, setSavingEditItem] = useState(false)
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

  useEffect(() => {
    if (!editItemForm) return undefined

    const previousOverflow = document.body.style.overflow
    document.body.style.overflow = 'hidden'

    const handleEscape = (event) => {
      if (event.key === 'Escape') setEditItemForm(null)
    }

    window.addEventListener('keydown', handleEscape)

    return () => {
      document.body.style.overflow = previousOverflow
      window.removeEventListener('keydown', handleEscape)
    }
  }, [editItemForm])

  const groupedMenu = useMemo(() => categorias.map((categoria) => ({
    ...categoria,
    itens: menu.filter((item) => item.categoria_id === categoria.id),
  })), [categorias, menu])

  const buildItemPayload = (form) => {
    if (!form.categoria_id) {
      throw new Error('Selecione uma categoria para o item.')
    }

    const payload = {
      item: form.item.trim(),
      valor: Number(form.valor),
      categoria_id: Number(form.categoria_id),
      imagem_base64: form.imagem_base64 || null,
    }

    if (!payload.item || !payload.valor) {
      throw new Error('Preencha nome e valor do item.')
    }

    return payload
  }

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
      const payload = buildItemPayload(itemForm)
      await criarItem(payload)
      setItemForm(initialItemForm)
      await load()
    } catch (error) {
      alert(error.response?.data?.detail || error.message || 'Não foi possível salvar o item.')
    } finally {
      setSavingItem(false)
    }
  }

  const submitEditItem = async (event) => {
    event.preventDefault()
    try {
      setSavingEditItem(true)
      const payload = buildItemPayload(editItemForm)
      await atualizarItem(editItemForm.id, payload)
      setEditItemForm(null)
      await load()
    } catch (error) {
      alert(error.response?.data?.detail || error.message || 'Não foi possível atualizar o item.')
    } finally {
      setSavingEditItem(false)
    }
  }

  const handleImageChange = async (event, setter) => {
    const file = event.target.files?.[0]
    if (!file) return
    const image = await readFileAsDataUrl(file)
    setter((prev) => ({ ...prev, imagem_base64: image }))
    event.target.value = ''
  }

  const openEditItemModal = (item) => {
    setEditItemForm(normalizeItemForm(item))
  }

  if (loading) {
    return <div className="page-shell"><div className="surface">Carregando painel gerencial...</div></div>
  }

  return (
    <>
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
                <p className="eyebrow">Novo item</p>
                <h2>Cadastrar itens com foto</h2>
              </div>
              <span className="pill">Edição via popup</span>
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
                <input type="file" accept="image/*" onChange={(event) => handleImageChange(event, setItemForm)} />
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
                  {savingItem ? 'Salvando...' : 'Criar item'}
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

                <div className="menu-grid menu-grid--uniform">
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
                            onClick={() => openEditItemModal(item)}
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

      {editItemForm && (
        <div className="modal-backdrop" onClick={() => setEditItemForm(null)}>
          <div className="modal-card" role="dialog" aria-modal="true" aria-labelledby="edit-item-title" onClick={(event) => event.stopPropagation()}>
            <div className="section-header section-header--compact modal-card__header">
              <div>
                <p className="eyebrow">Editar item</p>
                <h2 id="edit-item-title">{editItemForm.item || 'Atualizar produto do cardápio'}</h2>
              </div>
              <button type="button" className="modal-close" onClick={() => setEditItemForm(null)} aria-label="Fechar edição">
                ×
              </button>
            </div>

            <form className="form-grid" onSubmit={submitEditItem}>
              <label className="field field--full">
                <span>Nome do item</span>
                <input
                  value={editItemForm.item}
                  onChange={(event) => setEditItemForm((prev) => ({ ...prev, item: event.target.value }))}
                  placeholder="Nome do item"
                />
              </label>

              <label className="field">
                <span>Valor</span>
                <input
                  type="number"
                  min="0"
                  step="0.01"
                  value={editItemForm.valor}
                  onChange={(event) => setEditItemForm((prev) => ({ ...prev, valor: event.target.value }))}
                />
              </label>

              <label className="field">
                <span>Categoria</span>
                <select
                  value={editItemForm.categoria_id}
                  onChange={(event) => setEditItemForm((prev) => ({ ...prev, categoria_id: event.target.value }))}
                >
                  <option value="">Selecione...</option>
                  {categorias.map((categoria) => (
                    <option key={categoria.id} value={categoria.id}>{categoria.nome}</option>
                  ))}
                </select>
              </label>

              <label className="field field--full">
                <span>Substituir imagem do produto</span>
                <input type="file" accept="image/*" onChange={(event) => handleImageChange(event, setEditItemForm)} />
              </label>

              {editItemForm.imagem_base64 && (
                <div className="image-preview field--full">
                  <img src={editItemForm.imagem_base64} alt="Prévia da imagem do item" />
                  <div>
                    <strong>Prévia atual</strong>
                    <span className="helper-text">Ao salvar, a imagem mostrada aqui será aplicada ao item.</span>
                  </div>
                </div>
              )}

              <div className="form-actions form-actions--full modal-card__actions">
                <button type="button" className="ghost-button" onClick={() => setEditItemForm(null)}>
                  Cancelar
                </button>
                <button type="submit" className="primary-button" disabled={savingEditItem}>
                  {savingEditItem ? 'Salvando...' : 'Atualizar item'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  )
}
