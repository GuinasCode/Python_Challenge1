import { useState } from 'react'

export default function Login({ onLogin }) {
  const [login, setLogin] = useState('')
  const [senha, setSenha] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async () => {
    try {
      setLoading(true)
      await onLogin(login, senha)
    } catch (error) {
      alert(error.response?.data?.detail || 'Falha ao autenticar')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-screen">
      <div className="surface login-card">
        <div>
          <p className="eyebrow">RESTAURANTE</p>
          <h1>Acesso aos ambientes operacionais</h1>
          <p className="hero-copy">
            Entre com um perfil de garçom, cozinha, gerente ou administrador para testar os fluxos locais.
          </p>
        </div>

        <label className="field">
          <span>Login</span>
          <input placeholder="Login" value={login} onChange={(e) => setLogin(e.target.value)} />
        </label>

        <label className="field">
          <span>Senha</span>
          <input type="password" placeholder="Senha" value={senha} onChange={(e) => setSenha(e.target.value)} />
        </label>

        <button type="button" className="primary-button" onClick={handleSubmit} disabled={loading}>
          {loading ? 'Entrando...' : 'Entrar'}
        </button>

        <div className="stack-list__item">
          <div>
            <strong>Perfis de teste</strong>
            <span>admin, gerente, garcom e cozinha</span>
          </div>
          <span className="pill">seed local</span>
        </div>
      </div>
    </div>
  )
}
