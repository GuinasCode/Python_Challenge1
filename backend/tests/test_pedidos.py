def test_criar_pedido_valido(client, garcom_headers):
    response = client.post(
        "/pedidos",
        json={"nome_cliente": "João", "itens": [{"item_id": 1, "quantidade": 2}, {"item_id": 3, "quantidade": 1}]},
        headers=garcom_headers,
    )
    assert response.status_code == 201
    body = response.json()
    assert body["id"]
    assert body["valor_total"] == 74.8
    assert body["itens_detalhados"][0]["quantidade"] == 2


def test_criar_pedido_item_invalido(client, garcom_headers):
    response = client.post("/pedidos", json={"nome_cliente": "João", "itens": [999]}, headers=garcom_headers)
    assert response.status_code == 400


def test_criar_pedido_sem_cliente(client, garcom_headers):
    response = client.post("/pedidos", json={"itens": [1]}, headers=garcom_headers)
    assert response.status_code == 422


def test_avancar_status(client, cozinha_headers, garcom_headers):
    created = client.post("/pedidos", json={"nome_cliente": "Maria", "itens": [1]}, headers=garcom_headers).json()
    pedido_id = created["id"]
    r1 = client.patch(f"/pedidos/{pedido_id}/status", headers=cozinha_headers)
    assert r1.status_code == 200
    assert r1.json()["status"] == "Em preparo"
    r2 = client.patch(f"/pedidos/{pedido_id}/status", headers=cozinha_headers)
    assert r2.status_code == 200
    assert r2.json()["status"] == "Pronto"
    r3 = client.patch(f"/pedidos/{pedido_id}/status", headers=garcom_headers)
    assert r3.status_code == 200
    assert r3.json()["status"] == "Entregue"


def test_nao_avancar_entregue(client, cozinha_headers, garcom_headers):
    created = client.post("/pedidos", json={"nome_cliente": "Pedro", "itens": [1]}, headers=garcom_headers).json()
    pedido_id = created["id"]
    client.patch(f"/pedidos/{pedido_id}/status", headers=cozinha_headers)
    client.patch(f"/pedidos/{pedido_id}/status", headers=cozinha_headers)
    client.patch(f"/pedidos/{pedido_id}/status", headers=garcom_headers)
    response = client.patch(f"/pedidos/{pedido_id}/status", headers=garcom_headers)
    assert response.status_code == 400


def test_listar_pedidos_por_data(client, garcom_headers):
    client.post("/pedidos", json={"nome_cliente": "Data Test", "itens": [1]}, headers=garcom_headers)
    response = client.get("/pedidos?data=06/04/2026", headers=garcom_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_best_sellers_considera_quantidade(client, gerente_headers, garcom_headers):
    client.post(
        "/pedidos",
        json={"nome_cliente": "Ranking", "itens": [{"item_id": 1, "quantidade": 3}, {"item_id": 3, "quantidade": 2}]},
        headers=garcom_headers,
    )
    response = client.get("/relatorios/itens-mais-vendidos", headers=gerente_headers)
    assert response.status_code == 200
    assert response.json()[0]["quantidade"] >= 3
