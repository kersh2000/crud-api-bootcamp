from fastapi.testclient import TestClient
from fastapi import status
from server import app
from db import seed

client = TestClient(app)
seed.seed()

def test_homepage():
    response = client.get('/')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"Data" : "Go to the '/docs' endpoint to view all endpoints."}

def test_create_user():
    user = {
        "username": "testuser1",
        "password": "testpassword"
    }
    response = client.post("/users", json=user)

    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.json()


def test_get_user():
    user = {
        "username": "testuser2",
        "password": "testpassword"
    }
    response = client.post("/users", json=user)
    user_id = response.json()["id"]

    response = client.get(f"/users/{user_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == user["username"]
    assert response.json()["password"] == user["password"]


def test_update_user():
  response = client.post("/users", json={"username": "johndoe", "password": "password"})
  user_id = response.json()["id"]

  response = client.put(f"/users/{user_id}", json={"username": "janedoe", "password": "newpassword"})
  assert response.status_code == 200
  assert response.json() == {"message": "User updated successfully"}

  response = client.get(f"/users/{user_id}")
  assert response.status_code == 200
  assert response.json() == {"id": user_id, "username": "janedoe", "password": "newpassword"}

def test_delete_user():
    user = {
        "username": "testuser3",
        "password": "password!!!"
    }
    response = client.post("/users", json=user)
    user_id = response.json()["id"]

    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200

    assert response.json()["message"] == "User deleted successfully"

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404

