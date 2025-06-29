from main import app
from test.utils import *
from routers.admin import get_db,get_current_user
from fastapi.testclient import TestClient
from fastapi import status
from models import Todos

app.dependency_overrides[get_db]=override_get_db
app.dependency_overrides[get_current_user]=override_get_current_user

client=TestClient(app)

def test_admin_real_all_authenticated(test_todo):
    responce=client.get("/admin/todo")
    assert responce.status_code==status.HTTP_200_OK
    assert responce.json()==[{
    "id": 1,
    "title": "Learn to code",
    "description": "nil",
    "priority": 5,
    "complete": False,
    "owner_id": 1
    }]
    
def test_admin_delete_todo(test_todo):
    responce=client.delete("/todos/1")
    assert responce.status_code==status.HTTP_204_NO_CONTENT
    
    db=TestingSessionLocal()
    model=db.query(Todos).filter(Todos.id==1).first()
    assert model is None
    
def test_admin_delete_todo(test_todo):
    responce=client.delete("/todos/999")
    assert responce.status_code==404
    assert responce.json()=={
  "detail": "Todo Not found"
}