from fastapi import APIRouter, Request, Form, UploadFile, File, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db, user_data_save
from models import User, CandidateProfile
from schema.schema import UserSchema, Userlogindata, CandidateProfileSchema, CandidateProfileResponse
from user_auth import require_user
from admin_auth import require_admin
import admin_crud

router_frontend = APIRouter()

router_admin= APIRouter()

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "template") if os.path.exists(os.path.join(BASE_DIR, "template")) else "template"
templates = Jinja2Templates(directory=TEMPLATE_DIR)


@router_frontend.get("/")
def user_login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "title": "user login"
        }
    )

@router_frontend.get("/user_home")
def home_page(request: Request, user: User = Depends(require_user)):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={
            "title": "AI JOB search",
            "user": user
        }
    )

@router_frontend.get("/cv_details")
def cv_details_page(request: Request, user: User = Depends(require_user)):
    return templates.TemplateResponse(
        request=request,
        name="cv_extract.html",
        context={
            "title": "cv fetch",
            "user": user
        }
    )

@router_frontend.get("/chat")
def chat_page(request: Request, user: User = Depends(require_user)):
    return templates.TemplateResponse(
        request=request,
        name="chat.html",
        context={
            "title": "AI Job Assistant Chat",
            "user": user
        }
    )

@router_frontend.post("/submit_cv")
async def submit_cv(
    fullName: str = Form(...),
    email: str = Form(...),
    experience: str = Form(...),
    apifyKey: str = Form(...),
    groqKey: str = Form(...),
    cvFile: UploadFile = File(...),
    phone: str = Form(None),
    location: str = Form(None),
    jobTitle: str = Form(None),
    user: User = Depends(require_user),
    db: Session = Depends(get_db)
):
    try:
        # Backend validation using schema.py
        validated_data = CandidateProfileSchema(
            full_name=fullName,
            email=email,
            phone=phone,
            location=location,
            experience=experience,
            job_title=jobTitle,
            apify_key=apifyKey,
            groq_key=groqKey
        )

        # Save CV to static/cv and save candidate profile to DB
        profile = user_data_save(
            db=db,
            data=validated_data,
            cv_file=cvFile
        )

        return {
            "success": True,
            "message": "Profile submitted successfully!",
            "profile_id": profile.id,
            "cv_path": profile.cv_path
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router_frontend.post("/user/login/credential/")
def user_login_submit(
    request: Request,
    user: Userlogindata,
    db: Session = Depends(get_db)
):
    clean_username = user.username.strip() if user.username else ""
    clean_password = user.password.strip() if user.password else ""

    existing_user = db.query(User).filter(
        User.username == clean_username,
        User.password == clean_password
    ).first()

    if existing_user:
        request.session["user_id"] = existing_user.id
        request.session["username"] = existing_user.username
        request.session["is_staff"] = existing_user.is_staff

        return {
            "success": True,
            "message": "Login successful",
            "redirect_url": "user_home"
        }

    raise HTTPException(
        status_code=401,
        detail="Invalid username or password"
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
def admin_home_page(request: Request,admin: User = Depends(require_admin)):
    return templates.TemplateResponse(
        request=request,
        name="admin/adminhome.html",
        context={
            "title": "admin pabel"
        }
    )


# ==========================================
# ADMIN CRUD & AUTH LOGIC
# ==========================================

@router_frontend.get("/logout")
@router_frontend.get("/logout/")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(
        url="/admin_login",
        status_code=302
    )

@router_admin.post("/admin/data_submit", response_model=UserSchema)
def data_submit(user: UserSchema, db: Session = Depends(get_db)):
    return admin_crud.create_user(db=db, user=user)

@router_admin.get("/admin/users")
def get_users(db: Session = Depends(get_db)):
    return admin_crud.get_all_users(db=db)

@router_admin.get("/admin/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    return admin_crud.get_user_by_id(db=db, user_id=user_id)

@router_admin.put("/admin/users/{user_id}")
def update_user(
    user_id: int,
    user_data: UserSchema,
    db: Session = Depends(get_db)
):
    return admin_crud.update_user_by_id(db=db, user_id=user_id, user_data=user_data)

@router_admin.delete("/admin/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return admin_crud.delete_user_by_id(db=db, user_id=user_id)

@router_admin.post("/admin/login/credential/")
def admin_login_submit(
    request: Request,
    user: Userlogindata,
    db: Session = Depends(get_db)
):
    admin_user = admin_crud.authenticate_admin(db=db, user_data=user)

    request.session["user_id"] = admin_user.id
    request.session["username"] = admin_user.username
    request.session["is_staff"] = admin_user.is_staff

    return {
        "success": True,
        "redirect_url": "/admin/home"
    }
