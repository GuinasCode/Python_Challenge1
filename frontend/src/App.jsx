import { Navigate, Route, Routes, useNavigate } from 'react-router-dom'
import { useMemo, useState } from 'react'
import Cozinha from './pages/Cozinha'
import Garcom from './pages/Garcom'
import Gerencia from './pages/Gerencia'
import Login from './pages/Login'
import { login, setAuthToken } from './services/api'

function resolveHome(perfil) {
  if (perfil === 'garcom') return '/garcom'
  if (perfil === 'cozinha') return '/cozinha'
  if (['admin', 'gerente'].includes(perfil)) return '/gerencia'
  return '/login'
}

export default function App() {
  const [perfil, setPerfil] = useState(localStorage.getItem('perfil'))
  const navigate = useNavigate()
  const homePath = useMemo(() => resolveHome(perfil), [perfil])

  const handleLogin = async (usuario, senha) => {
    const resp = await login(usuario, senha)
    localStorage.setItem('token', resp.data.access_token)
    localStorage.setItem('perfil', resp.data.perfil)
    setAuthToken(resp.data.access_token)
    setPerfil(resp.data.perfil)
    navigate(resolveHome(resp.data.perfil))
  }

  return (
    <Routes>
      <Route path="/" element={<Navigate to={homePath} replace />} />
      <Route path="/login" element={<Login onLogin={handleLogin} />} />
      <Route path="/garcom" element={perfil === 'garcom' ? <Garcom /> : <Navigate to="/login" replace />} />
      <Route path="/cozinha" element={perfil === 'cozinha' ? <Cozinha /> : <Navigate to="/login" replace />} />
      <Route path="/gerencia" element={['admin', 'gerente'].includes(perfil) ? <Gerencia /> : <Navigate to="/login" replace />} />
    </Routes>
  )
}
