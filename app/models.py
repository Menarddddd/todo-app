from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from .database import Base
from sqlalchemy.orm import relationship



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String)
    password = Column(String)
    
    todos = relationship("Todo", back_populates="author")


class Todo(Base):
    __tablename__ = "todos" 

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    due_date = Column(DateTime)
    status = Column(Boolean)
    user_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User", back_populates="todos")