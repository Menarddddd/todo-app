from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime



class LoginData(BaseModel):
    username: str
    password: str


class UserCreate(BaseModel):
    name: str
    username: str
    password: str


class UpdateUser(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TodoCreate(BaseModel):
    title: str
    description: str
    due_date: datetime
    status: bool
    
class TodoResponse(BaseModel):
    id: int
    title: str
    description: str
    due_date: datetime
    status: bool
    user_id: int

    model_config = ConfigDict(from_attributes=True)

class TodoProfileResponse(BaseModel):
    id: int
    title: str
    description: str
    due_date: datetime
    status: bool

    model_config = ConfigDict(from_attributes=True)
