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