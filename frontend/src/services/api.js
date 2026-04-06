import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
})

export function setAuthToken(token) {
  if (token) api.defaults.headers.common.Authorization = `Bearer ${token}`
  else delete api.defaults.headers.common.Authorization
}

if (typeof window !== 'undefined') {
  setAuthToken(window.localStorage.getItem('token'))
}

export const login = (login, senha) => api.post('/auth/login', { login, senha })
export const me = () => api.get('/auth/me')

export const listarCategorias = () => api.get('/categorias')
export const criarCategoria = (payload) => api.post('/categorias', payload)
export const atualizarCategoria = (id, payload) => api.put(`/categorias/${id}`, payload)
export const removerCategoria = (id) => api.delete(`/categorias/${id}`)

export const listarMenu = () => api.get('/menu')
export const criarItem = (payload) => api.post('/menu', payload)
export const atualizarItem = (id, payload) => api.put(`/menu/${id}`, payload)
export const removerItem = (id) => api.delete(`/menu/${id}`)

export const criarPedido = (payload) => api.post('/pedidos', payload)
export const listarPedidos = (params) => api.get('/pedidos', { params })
export const listarPendentes = () => api.get('/pedidos/pendentes')
export const avancarStatus = (id) => api.patch(`/pedidos/${id}/status`)

export const receita = (inicio, fim) => api.get('/relatorios/receita', { params: { inicio, fim } })

export default api
