def test_listar_menu(client, garcom_headers):
    response = client.get("/menu", headers=garcom_headers)
    assert response.status_code == 200
    body = response.json()
    assert len(body) >= 1
    assert body[0]["categoria_nome"]
    assert body[0]["imagem_base64"].startswith("data:image/")


def test_adicionar_item_gerente(client, gerente_headers):
    categorias = client.get("/categorias", headers=gerente_headers).json()
    bebidas = next(c for c in categorias if c["nome"] == "Bebidas")
    response = client.post(
        "/menu",
        json={"item": "Chá Gelado", "valor": 12.5, "categoria_id": bebidas["id"]},
        headers=gerente_headers,
    )
    assert response.status_code == 201
    assert response.json()["item"] == "Chá Gelado"
    assert response.json()["categoria_nome"] == "Bebidas"


def test_adicionar_item_garcom(client, garcom_headers):
    response = client.post("/menu", json={"item": "Não pode", "valor": 10}, headers=garcom_headers)
    assert response.status_code == 403


def test_editar_item(client, gerente_headers):
    categorias = client.get("/categorias", headers=gerente_headers).json()
    sobremesas = next(c for c in categorias if c["nome"] == "Sobremesas")
    response = client.put(
        "/menu/1",
        json={"item": "Frango Premium", "valor": 50.0, "categoria_id": sobremesas["id"]},
        headers=gerente_headers,
    )
    assert response.status_code == 200
    assert response.json()["item"] == "Frango Premium"
    assert response.json()["categoria_nome"] == "Sobremesas"


def test_deletar_item(client, admin_headers):
    response = client.delete("/menu/1", headers=admin_headers)
    assert response.status_code == 204
