from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from database import Base
import pytest 
from models import Todos, Users
from routers.auth import bcrypt_context

SQLALCHEMY_DATABASE_URL="sqlite:///./testdb.db"

engine=create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread":False},
    poolclass=StaticPool
)

TestingSessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db=TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username':'atharv','id':1,'user_role':'admin'}  

@pytest.fixture
def test_todo():
    todo=Todos(
        title="Learn to code",
        description="nil",
        priority="5",
        complete=False,
        owner_id=1
    )
    
    db=TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()
        
@pytest.fixture
def test_users():
    user=Users(
        user="atharv",
        email="email@a.com",
        first_name="atharv",
        last_name="sharma",
        hashed_password=bcrypt_context.hash("hello"),
        role="admin"
    )
    
    db=TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()