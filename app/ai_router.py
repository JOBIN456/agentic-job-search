from resume_fetch import fetch_resume
from fastapi import APIRouter, Request, Form, UploadFile, File, HTTPException, Depends

ai_router = APIRouter()