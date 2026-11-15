from fastapi import FastAPI
import router

from fastapi.staticfiles import StaticFiles
from database import Base, engine
from models import User, CandidateProfile
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
import os
load_dotenv()
Fastapi_auth = os.getenv("Fastapi_Auth")

Base.metadata.create_all(bind=engine)
app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static") if os.path.exists(os.path.join(BASE_DIR, "static")) else "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


app.include_router(router.router_frontend)
app.include_router(router.router_admin)


app.add_middleware(
    SessionMiddleware,
    secret_key="Fastapi_auth"
)