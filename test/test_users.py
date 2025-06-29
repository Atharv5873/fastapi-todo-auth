from test.utils import *
from routers.users import get_db,get_current_user
from fastapi import status
from fastapi.testclient import TestClient
from main import app

app.dependency_overrides[get_db]=override_get_db
app.dependency_overrides[override_get_current_user]=override_get_current_user

client=client=TestClient(app)

def test_return_user(test_users):
    responce=client.get("/user")
    assert responce.json()['user'] == "atharv"
    assert responce.json()['email'] == "email@a.com"
    assert responce.json()['first_name'] == "atharv"
    assert responce.json()['last_name'] == "sharma"
    assert responce.json()['role'] == "admin"