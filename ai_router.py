from resume_fetch import fetch_resume
from fastapi import APIRouter, Request, Form, UploadFile, File, HTTPException, Depends

router_ai = APIRouter()