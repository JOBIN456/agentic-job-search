import os
import uuid
import shutil
from datetime import datetime
from typing import Optional
from fastapi import Form, File, UploadFile, HTTPException
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session
from models import CandidateProfile

# Server directory where uploaded CV files are stored
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CV_UPLOAD_DIR = os.path.join(BASE_DIR, "static", "cv")
os.makedirs(CV_UPLOAD_DIR, exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx"}


# ---------------------------------------------------------------------------
# Pydantic Schemas for Form Validation & Response
# ---------------------------------------------------------------------------
class CandidateProfileForm(BaseModel):
    full_name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    phone: Optional[str] = None
    location: Optional[str] = None
    experience: str
    job_title: Optional[str] = None
    apify_key: str = Field(..., min_length=5, max_length=100)
    groq_key: str = Field(..., min_length=5, max_length=100)


class CandidateProfileResponse(BaseModel):
    id: int
    full_name: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    experience: str
    job_title: Optional[str] = None
    apify_key: str
    groq_key: str
    cv_path: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# CV File Storage Helper
# ---------------------------------------------------------------------------
def save_cv_file(file: UploadFile) -> str:
    """
    Saves the uploaded CV file to the server's 'static/cv' folder.
    Returns the relative URL path to be saved in the database (e.g. '/static/cv/abc12345_cv.pdf').
    The PDF file itself is stored on the server filesystem, NOT inside the database.
    """
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="CV file is required.")

    # Validate file extension
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Only PDF, DOC, and DOCX files are allowed."
        )

    # Generate a unique, safe filename
    original_basename = os.path.splitext(os.path.basename(file.filename))[0]
    safe_name = "".join(c for c in original_basename if c.isalnum() or c in ("-", "_")).strip() or "cv"
    unique_filename = f"{uuid.uuid4().hex[:8]}_{safe_name}{ext}"
    destination_path = os.path.join(CV_UPLOAD_DIR, unique_filename)

    # Save the file to server filesystem
    try:
        with open(destination_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save CV on server: {str(e)}")

    # Return the URL path to save into the database
    url_path = f"/static/cv/{unique_filename}"
    return url_path


# ---------------------------------------------------------------------------
# Database Service Helper
# ---------------------------------------------------------------------------
def create_candidate_profile(
    db: Session,
    full_name: str,
    email: str,
    experience: str,
    apify_key: str,
    groq_key: str,
    cv_file: UploadFile,
    phone: Optional[str] = None,
    location: Optional[str] = None,
    job_title: Optional[str] = None,
) -> CandidateProfile:
    """
    1. Saves the uploaded CV file to the server cv folder.
    2. Inserts candidate profile record with the CV's URL path in the DB.
    """
    # 1. Store CV on server and get URL path
    cv_url_path = save_cv_file(cv_file)

    # 2. Create and store database record
    profile = CandidateProfile(
        full_name=full_name,
        email=email,
        phone=phone,
        location=location,
        experience=experience,
        job_title=job_title,
        apify_key=apify_key,
        groq_key=groq_key,
        cv_path=cv_url_path  # Only the URL path is saved in the database
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

