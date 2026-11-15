from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserSchema(BaseModel):
    id: int | None = None
    username: str
    password: str
    is_staff: bool = False

    class Config:
        from_attributes = True


class Userlogindata(BaseModel):
    id: int | None = None
    username: str
    password: str

    class Config:
        from_attributes = True


class CandidateProfileSchema(BaseModel):
    full_name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    phone: Optional[str] = None
    location: Optional[str] = None
    experience: str
    job_title: Optional[str] = None
    apify_key: str = Field(..., min_length=5, max_length=100)
    groq_key: str = Field(..., min_length=5, max_length=100)

    class Config:
        from_attributes = True


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


# Aliases for convenience
CandidateProfileForm = CandidateProfileSchema



class CandidateProfileSchema(BaseModel):
    full_name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    phone: Optional[str] = None
    location: Optional[str] = None
    experience: str
    job_title: Optional[str] = None
    apify_key: str = Field(..., min_length=5, max_length=100)
    groq_key: str = Field(..., min_length=5, max_length=100)

    class Config:
        from_attributes = True


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


# Aliases for convenience
CandidateProfileForm = CandidateProfileSchema