from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from starlette import status
from models import Todos, Users
from database import SessionLocal
from typing import Annotated
from .auth import get_current_user
from passlib.context import CryptContext
from fastapi import Body

router=APIRouter(
    prefix='/user',
    tags=['Users']
)


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
class UserVerification(BaseModel):
    password:str
    new_password:str=Field(min_length=6)

db_dependency=Annotated[Session,Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_current_user)]
bcrypt_context=CryptContext(schemes=['bcrypt'], deprecated='auto')

@router.get('/',status_code=status.HTTP_200_OK)
async def get_users(user:user_dependency,db:db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Authentication Failure')
    return db.query(Users).filter(Users.id==user.get('id')).first()

@router.put('/password',status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user:user_dependency,db:db_dependency,user_verification:UserVerification=Body(...)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Authentication Failure')
    user_model=db.query(Users).filter(Users.id==user.get('id')).first()
    if not bcrypt_context.verify(user_verification.password,user_model.hashed_password):
        raise HTTPException(status_code=401,detail='Wrong Current Password Entered')
    user_model.hashed_password=bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()
    