from fastapi import FastAPI
import router

from fastapi.staticfiles import StaticFiles
from database import Base, engine
from  models import User

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(router.router_frontend)