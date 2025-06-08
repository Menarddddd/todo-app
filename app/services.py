from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi import status, HTTPException

from app.hashing import hash_password, verify_password
from app.oauth import create_access_token
from app.schemas import TodoCreate, UpdateUser, UserCreate
from .models import Todo, User



def check_username(username, db: Session):
    if len(username) < 6:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username must be atleast 6.")
    same_username = db.query(User).filter(User.username == username).first()
    if same_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username is already use.")
    return 

def check_password(password):
    return any(char.isdigit() for char in password)


def check_updated(username: str | None, password: str | None, db: Session, current_username: str):
    # Validate username if provided
    if username:
        if len(username) < 6:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username must be at least 6 characters.")
        
        # Check for existing username excluding current user
        same_username = db.query(User).filter(User.username == username).filter(User.username != current_username).first()
        if same_username:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username is already in use.")

    # Validate password if provided
    if password:
        if not any(char.isdigit() for char in password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must contain at least 1 number.")


def login_token_service(form_data: OAuth2PasswordRequestForm, db: Session):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not found.")
    
    check_pwd = verify_password(form_data.password, user.password)
    if not check_pwd:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Username or password is incorrect.")
    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


def sign_up_services(data: UserCreate, db: Session):
    check_username(data.username, db)

    has_int = check_password(data.password)

    if not has_int:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must contain atleast 1 number")

    new_hash_password = hash_password(data.password)

    new_user = User(
        name = data.name,
        username = data.username,
        password = new_hash_password
    )

    db.add(new_user)
    db.commit()
    return f"Username {data.username} has been created."


def profile_service(db: Session, current_user):
    user = db.query(User).filter(User.username == current_user["username"]).first()
    todos = db.query(Todo).all()
    my_todos = []
    for todo in todos:
        if (todo.user_id == user.id):
            my_todos.append(todo)
    return my_todos


def update_account(update_data: UpdateUser, db: Session, current_user):
    user = db.query(User).filter(User.username == current_user["username"]).first()

    input_data = update_data.model_dump(exclude_unset=True)
    check_updated(
        username=input_data.get("username"),
        password=input_data.get("password"),
        db=db,
        current_username=user.username
    )

    for key, value in input_data.items():
        if key == "password":
            value = hash_password(value)
        setattr(user, key, value)

    db.commit()
    return f"User {user.username} has been updated."


def delete_user_service(db: Session, current_user):
    user = db.query(User).filter(User.username == current_user["username"]).first()
    db.delete(user)
    db.commit()


def create_todo_service(todo_data: TodoCreate, db: Session, current_user):
    user = db.query(User).filter(User.username == current_user["username"]).first()
    get_user_id = user.id

    new_todo = Todo(
        title = todo_data.title,
        description = todo_data.description,
        due_date = todo_data.due_date,
        status = todo_data.status,
        user_id = get_user_id
    )

    db.add(new_todo)
    db.commit()
    return f"Todo {todo_data.title} has been created."


def delete_todo_service(id, db: Session, current_user):
    user = db.query(User).filter(User.username == current_user["username"]).first()
    todo = db.query(Todo).filter(Todo.id == id).first()
    if todo.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Todo is not yours!")

    db.delete(todo)
    db.commit()
    return f"Todo {todo.title} has been deleted."


