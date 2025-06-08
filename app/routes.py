from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .schemas import TodoCreate, UserCreate, Token, TodoResponse, TodoProfileResponse, UpdateUser
from .models import User, Todo
from fastapi.security import OAuth2PasswordRequestForm
from .database import get_db
from .hashing import hash_password, verify_password
from .oauth import create_access_token, get_current_user
from .services import check_username, check_password, check_updated, create_todo_service, delete_todo_service, delete_user_service, login_token_service, profile_service, sign_up_services



route = APIRouter()


@route.post("/token", response_model=Token, status_code=status.HTTP_200_OK)
def login_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return login_token_service(form_data, db)


@route.post("/signup", status_code=status.HTTP_201_CREATED)
def sign_up(data: UserCreate, db: Session = Depends(get_db)):
    return sign_up_services(data, db)



@route.get("/profile", response_model=List[TodoProfileResponse], status_code=status.HTTP_200_OK)
def profile(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return profile_service(db, current_user)


@route.get("/home", response_model=List[TodoResponse], status_code=status.HTTP_200_OK)
def home(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(Todo).all()



@route.put("/update_account", status_code=status.HTTP_200_OK)
def update_account(update_data: UpdateUser, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return update_account(update_data, db, current_user)



@route.delete("/delete_user", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return delete_user_service(db, current_user)



# todo 

@route.post("/create_todo")
def create_todo(todo_data: TodoCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return create_todo_service(todo_data, db, current_user)


@route.delete("/delete_todo/{id}")
def delete_todo(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return delete_todo_service(id, db, current_user)
