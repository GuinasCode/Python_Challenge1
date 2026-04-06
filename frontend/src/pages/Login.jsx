import { useState } from 'react'

export default function Login({ onLogin }) {
  const [login, setLogin] = useState('')
  const [senha, setSenha] = useState('')

  return (
    <div>
      <h1>Login</h1>
      <input placeholder="Login" value={login} onChange={(e) => setLogin(e.target.value)} />
      <input type="password" placeholder="Senha" value={senha} onChange={(e) => setSenha(e.target.value)} />
      <button onClick={() => onLogin(login, senha)}>Entrar</button>
    </div>
  )
}
