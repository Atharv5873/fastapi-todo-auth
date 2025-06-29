from main import app
from routers.todos import get_db, get_current_user
from fastapi.testclient import TestClient
from fastapi import status
from models import Todos
from test.utils import *

app.dependency_overrides[get_db]=override_get_db
app.dependency_overrides[get_current_user]=override_get_current_user

client=TestClient(app)

def test_read_all_authenticated(test_todo):
    responce=client.get("/")
    assert responce.status_code == status.HTTP_200_OK
    assert responce.json()==[
  {
    "id": 1,
    "title": "Learn to code",
    "description": "nil",
    "priority": 5,
    "complete": False,
    "owner_id": 1
  }
]

def test_read_one_authenticated(test_todo):
    responce=client.get("/todo/1")
    assert responce.status_code == status.HTTP_200_OK
    assert responce.json()=={
    "id": 1,
    "title": "Learn to code",
    "description": "nil",
    "priority": 5,
    "complete": False,
    "owner_id": 1
    }

def test_read_one_authenticated_not_found():
    responce=client.get("/todo/999")
    assert responce.status_code==status.HTTP_404_NOT_FOUND
    assert responce.json()=={
    "detail": "TODO not found"
    }
    
def test_create_todo(test_todo):
    request_data={
        'title':'new todo',
        'description':'new todo',
        'priority':5,
        'complete':False
    }

    responce=client.post('/todo/',json=request_data)
    assert responce.status_code == 201
    db=TestingSessionLocal()
    model=db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.complete == request_data.get('complete')
    assert model.priority == request_data.get('priority')
    
def test_update_todo(test_todo):
    request_data={
        'title':'changed todo',
        'description':'changed todo',
        'priority':5,
        'complete':True
    }
    
    responce=client.put('/todos/update_todo/1',json=request_data)
    assert responce.status_code==204
    db=TestingSessionLocal()
    model=db.query(Todos).filter(Todos.id==1).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.complete == request_data.get('complete')
    assert model.priority == request_data.get('priority')
    
def test_update_todo_not_found(test_todo):
    request_data={
        'title':'changed todo',
        'description':'changed todo',
        'priority':5,
        'complete':True
    }
    
    responce=client.put('/todos/update_todo/999',json=request_data)
    assert responce.status_code==404
    assert responce.json()=={
  "detail": "Todo Not found"
}
    
def test_delete_todo(test_todo):
    responce=client.delete('/todos/1')
    assert responce.status_code==204
    db=TestingSessionLocal()
    model=db.query(Todos).filter(Todos.id==1).first()
    assert model is None
    
def test_delete_todo_not_found(test_todo):
    responce=client.delete('/todos/999')
    assert responce.status_code==404
    assert responce.json()=={
  "detail": "Todo Not found"
}