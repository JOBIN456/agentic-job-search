from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

router_frontend = APIRouter()

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