from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schema.schema import UserSchema


router_frontend = APIRouter()

router_admin= APIRouter()

templates = Jinja2Templates(directory="template")

@router_frontend.get("/")
def home_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={
            "title": "AI JOB search"
        }
    )

@router_frontend.get("/cv_details")
def home_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="cv_extract.html",
        context={
            "title": "cv fetch"
        }
    )

@router_frontend.get("/user_login")
def user_login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "title": "user login"
        }
    )


@router_frontend.get("/admin_login")
def admin_login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="admin/adminlogin.html",
        context={
            "title": "admin login"
        }
    )


@router_frontend.get("/admin/home")
def admin_home_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="admin/adminhome.html",
        context={
            "title": "admin pabel"
        }
    )


# ADMIN LOGIC
@router_admin.post("/admin/data_submit", response_model=UserSchema)
def data_submit(user: UserSchema, db: Session = Depends(get_db)):

    # Check if username already exists
    existing_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists in DB"
        )

    # Create user
    new_user = User(
        username=user.username,
        password=user.password,
        is_staff=user.is_staff
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router_admin.get("/admin/users")
def get_users(db: Session = Depends(get_db)):

    users = db.query(User).all()

    return [
        {
            "id": user.id,
            "username": user.username,
            "is_staff": user.is_staff
        }
        for user in users
    ]

@router_admin.get("/admin/users")
def get_users(db: Session = Depends(get_db)):

    users = db.query(User).all()

    return [
        {
            "id": user.id,
            "username": user.username,
            "is_staff": user.is_staff
        }
        for user in users
    ]

@router_admin.get("/admin/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "id": user.id,
        "username": user.username,
        "password":user.password,
        "is_staff": user.is_staff
    }