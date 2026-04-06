import { Navigate, Route, Routes, useNavigate } from 'react-router-dom'
import { useState } from 'react'
import Cozinha from './pages/Cozinha'
import Garcom from './pages/Garcom'
import Gerencia from './pages/Gerencia'
import Login from './pages/Login'
import { login, setAuthToken } from './services/api'

export default function App() {
  const [perfil, setPerfil] = useState(localStorage.getItem('perfil'))
  const navigate = useNavigate()

  const handleLogin = async (usuario, senha) => {
    const resp = await login(usuario, senha)
    localStorage.setItem('token', resp.data.access_token)
    localStorage.setItem('perfil', resp.data.perfil)
    setAuthToken(resp.data.access_token)
    setPerfil(resp.data.perfil)
    if (resp.data.perfil === 'garcom') navigate('/garcom')
    else if (resp.data.perfil === 'cozinha') navigate('/cozinha')
    else navigate('/gerencia')
  }

  return (
    <Routes>
      <Route path="/" element={<Login onLogin={handleLogin} />} />
      <Route path="/login" element={<Login onLogin={handleLogin} />} />
      <Route path="/garcom" element={perfil === 'garcom' ? <Garcom /> : <Navigate to="/login" />} />
      <Route path="/cozinha" element={perfil === 'cozinha' ? <Cozinha /> : <Navigate to="/login" />} />
      <Route path="/gerencia" element={['admin', 'gerente'].includes(perfil) ? <Gerencia /> : <Navigate to="/login" />} />
    </Routes>
  )
}
