from fastapi import FastAPI
from . import routes
from .models import User, Todo
from .database import Base, engine


app = FastAPI()

app.include_router(routes.route)

Base.metadata.create_all(bind=engine)
