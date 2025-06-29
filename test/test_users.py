from test.utils import *
from routers.users import get_db,get_current_user
from fastapi import status
from fastapi.testclient import TestClient
from main import app

app.dependency_overrides[get_db]=override_get_db
app.dependency_overrides[override_get_current_user]=override_get_current_user

client=client=TestClient(app)

def test_return_user(test_users):
    response=client.get("/user")
    assert response.json()['user'] == "atharv"
    assert response.json()['email'] == "email@a.com"
    assert response.json()['first_name'] == "atharv"
    assert response.json()['last_name'] == "sharma"
    assert response.json()['role'] == "admin"
    
def test_change_password(test_users):
    response = client.put("/user/password",json={"password": "hello",
                           "new_password": "testeeee"})
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_change_password_invalid_password(test_users):
    response = client.put("/user/password",json={"password": "testeeee",
                           "new_password": "hellllll"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED