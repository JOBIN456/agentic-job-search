from fastapi import APIRouter, Request, Form, UploadFile, File, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
from models import User, CandidateProfile
from schema.schema import UserSchema, Userlogindata
from form import create_candidate_profile


router_frontend = APIRouter()

router_admin= APIRouter()

templates = Jinja2Templates(directory="template")


def require_admin(
    request: Request,
    db: Session = Depends(get_db)
):
    user_id = request.session.get("user_id")

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Please log in first"
        )

    user = db.query(User).filter(
        User.id == user_id,
        User.is_staff == True
    ).first()

    if not user:
        request.session.clear()
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return user
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
    bio: str = Form(None),
    db: Session = Depends(get_db)
):
    try:
        profile = create_candidate_profile(
            db=db,
            full_name=fullName,
            email=email,
            phone=phone,
            location=location,
            experience=experience,
            job_title=jobTitle,
            apify_key=apifyKey,
            groq_key=groqKey,
            bio=bio,
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
def admin_home_page(request: Request,admin: User = Depends(require_admin)):
    return templates.TemplateResponse(
        request=request,
        name="admin/adminhome.html",
        context={
            "title": "admin pabel"
        }
    )


# ADMIN LOGIC

@router_frontend.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(
        url="/user_login",
        status_code=302
    )   

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


@router_admin.delete("/admin/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(user)
    db.commit()

    return {
        "message": "User deleted successfully",
        "id": user_id
    }

@router_admin.put("/admin/users/{user_id}")
def update_user(
    user_id: int,
    user_data: UserSchema,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Check if username is being changed
    existing_user = db.query(User).filter(
        User.username == user_data.username,
        User.id != user_id
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists in DB"
        )

    # Update user
    user.username = user_data.username
    user.password = user_data.password
    user.is_staff = user_data.is_staff

    db.commit()
    db.refresh(user)

    return {
        "message": "User updated successfully",
        "id": user.id,
        "username": user.username,
        "is_staff": user.is_staff
    }

@router_admin.post("/admin/login/credential/")
def data_submit(
    request: Request,
    user: Userlogindata,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.username == user.username,
        User.password == user.password,
        User.is_staff == True
    ).first()

    if existing_user:
        request.session["user_id"] = existing_user.id

        return {
            "success": True,
            "redirect_url": "/admin/home"
        }

    raise HTTPException(
        status_code=401,
        detail="Invalid username or password"
    )
