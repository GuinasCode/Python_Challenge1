import { useEffect, useState } from 'react'
import PainelCozinha from '../components/PainelCozinha'
import { avancarStatus, listarPendentes } from '../services/api'

export default function Cozinha() {
  const [pedidos, setPedidos] = useState([])

  const load = async () => {
    const resp = await listarPendentes()
    setPedidos(resp.data)
  }

  useEffect(() => {
    load()
    const t = setInterval(load, 30000)
    return () => clearInterval(t)
  }, [])

  return <PainelCozinha pedidos={pedidos} onAvancar={async (id) => { await avancarStatus(id); load() }} />
}
