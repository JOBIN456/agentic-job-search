import os
import uuid
import shutil
from typing import Optional, Union
from fastapi import UploadFile, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# Server directory where database and uploaded CV files are stored
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "app.db")
DATABASE_URL = f"sqlite:///{DB_FILE.replace(os.sep, '/')}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Server directory where uploaded CV files are stored
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CV_UPLOAD_DIR = os.path.join(BASE_DIR, "static", "cv")
os.makedirs(CV_UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx"}


def user_data_save(
    db: Session,
    data,
    cv_file: UploadFile,
    **kwargs
):
    """
    Saves the uploaded CV file to the server's 'static/cv' folder,
    and saves candidate profile data along with the CV URL path to the database.
    """
    if not cv_file or not cv_file.filename:
        raise HTTPException(status_code=400, detail="CV file is required.")

    # Validate file extension
    ext = os.path.splitext(cv_file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Only PDF, DOC, and DOCX files are allowed."
        )

    # Generate a unique, safe filename
    original_basename = os.path.splitext(os.path.basename(cv_file.filename))[0]
    safe_name = "".join(c for c in original_basename if c.isalnum() or c in ("-", "_")).strip() or "cv"
    unique_filename = f"{uuid.uuid4().hex[:8]}_{safe_name}{ext}"
    destination_path = os.path.join(CV_UPLOAD_DIR, unique_filename)

    # Save file to disk
    try:
        with open(destination_path, "wb") as buffer:
            shutil.copyfileobj(cv_file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save CV on server: {str(e)}")

    # Relative URL path to be saved in the database
    cv_url_path = f"/static/cv/{unique_filename}"

    # Extract field values from schema object or dict
    if hasattr(data, "model_dump"):
        data_dict = data.model_dump()
    elif hasattr(data, "dict"):
        data_dict = data.dict()
    elif isinstance(data, dict):
        data_dict = data
    else:
        data_dict = kwargs

    from models import CandidateProfile

    profile = CandidateProfile(
        full_name=data_dict.get("full_name") or kwargs.get("full_name"),
        email=str(data_dict.get("email") or kwargs.get("email")),
        phone=data_dict.get("phone") or kwargs.get("phone"),
        location=data_dict.get("location") or kwargs.get("location"),
        experience=data_dict.get("experience") or kwargs.get("experience"),
        job_title=data_dict.get("job_title") or kwargs.get("job_title"),
        apify_key=data_dict.get("apify_key") or kwargs.get("apify_key"),
        groq_key=data_dict.get("groq_key") or kwargs.get("groq_key"),
        cv_path=cv_url_path
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile
