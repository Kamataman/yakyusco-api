import copy
from fastapi.testclient import TestClient

from yakyusco_api.main import app

client = TestClient(app)

team_id="jesus"
create_data = {"name": "foobar", "number": "011", "team_id": team_id}
created_data = None


def test_create_player():
    response = client.post(
        "/players/",
        headers={"X-Token": "coneofsilence"},
        json=create_data,
    )
    assert response.status_code == 200
    response_data = response.json()
    assert type(response_data["id"]) == int
    created_data = copy.copy(create_data)
    created_data["id"] = response_data["id"]
    print(f"created_data: {created_data}")
    assert response_data["name"] == create_data["name"]
    assert response_data["number"] == create_data["number"]


def test_read_player():
    response = client.get(f"/players/${created_data["id"]}", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    assert response.json().find(created_data)


# def test_read_item_bad_token():
#     response = client.get("/items/foo", headers={"X-Token": "hailhydra"})
#     assert response.status_code == 400
#     assert response.json() == {"detail": "Invalid X-Token header"}


# def test_read_nonexistent_item():
#     response = client.get("/items/baz", headers={"X-Token": "coneofsilence"})
#     assert response.status_code == 404
#     assert response.json() == {"detail": "Item not found"}


# def test_create_item_bad_token():
#     response = client.post(
#         "/items/",
#         headers={"X-Token": "hailhydra"},
#         json={"id": "bazz", "title": "Bazz", "description": "Drop the bazz"},
#     )
#     assert response.status_code == 400
#     assert response.json() == {"detail": "Invalid X-Token header"}


# def test_create_existing_item():
#     response = client.post(
#         "/items/",
#         headers={"X-Token": "coneofsilence"},
#         json={
#             "id": "foo",
#             "title": "The Foo ID Stealers",
#             "description": "There goes my stealer",
#         },
#     )
#     assert response.status_code == 409
#     assert response.json() == {"detail": "Item already exists"}
