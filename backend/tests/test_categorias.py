def test_listar_categorias(client, gerente_headers):
    response = client.get("/categorias", headers=gerente_headers)
    assert response.status_code == 200
    assert any(item["nome"] == "Bebidas" for item in response.json())


def test_criar_categoria(client, gerente_headers):
    response = client.post(
        "/categorias",
        json={"nome": "Entradas", "ordem": 4},
        headers=gerente_headers,
    )
    assert response.status_code == 201
    assert response.json()["nome"] == "Entradas"


def test_nao_remover_categoria_com_itens(client, admin_headers):
    categorias = client.get("/categorias", headers=admin_headers).json()
    pratos = next(c for c in categorias if c["nome"] == "Pratos executivos")
    response = client.delete(f"/categorias/{pratos['id']}", headers=admin_headers)
    assert response.status_code == 400
