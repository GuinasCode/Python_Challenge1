def test_listar_menu(client, garcom_headers):
    response = client.get("/menu", headers=garcom_headers)
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_adicionar_item_gerente(client, gerente_headers):
    response = client.post("/menu", json={"item": "Novo Prato", "valor": 39.9}, headers=gerente_headers)
    assert response.status_code == 201
    assert response.json()["item"] == "Novo Prato"


def test_adicionar_item_garcom(client, garcom_headers):
    response = client.post("/menu", json={"item": "Não pode", "valor": 10}, headers=garcom_headers)
    assert response.status_code == 403


def test_editar_item(client, gerente_headers):
    response = client.put("/menu/1", json={"item": "Frango Premium", "valor": 50.0}, headers=gerente_headers)
    assert response.status_code == 200
    assert response.json()["item"] == "Frango Premium"


def test_deletar_item(client, admin_headers):
    response = client.delete("/menu/1", headers=admin_headers)
    assert response.status_code == 204
