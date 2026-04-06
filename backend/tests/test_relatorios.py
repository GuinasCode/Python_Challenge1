def test_receita_requer_perfil_gerencial(client, garcom_headers):
    response = client.get("/relatorios/receita", headers=garcom_headers)
    assert response.status_code == 403


def test_receita_gerente(client, gerente_headers, garcom_headers):
    client.post("/pedidos", json={"nome_cliente": "R1", "itens": [1, 2]}, headers=garcom_headers)
    response = client.get("/relatorios/receita?inicio=06/04/2026&fim=06/04/2026", headers=gerente_headers)
    assert response.status_code == 200
    assert "total" in response.json()
