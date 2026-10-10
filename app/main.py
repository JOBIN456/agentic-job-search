from fastapi import FastAPI
import router

from fastapi.staticfiles import StaticFiles
from database import Base, engine
from  models import User
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
import os
load_dotenv()
Fastapi_auth = os.getenv("Fastapi_Auth")

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(router.router_frontend)
app.include_router(router.router_admin)


app.add_middleware(
    SessionMiddleware,
    secret_key="Fastapi_auth"
)