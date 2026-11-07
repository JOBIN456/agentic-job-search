from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_staff = Column(Boolean, default=False)


class CandidateProfile(Base):
    __tablename__ = "candidate_profiles"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, index=True)
    phone = Column(String(30), nullable=True)
    location = Column(String(100), nullable=True)
    experience = Column(String(50), nullable=False)
    job_title = Column(String(100), nullable=True)
    apify_key = Column(String(255), nullable=False)
    groq_key = Column(String(255), nullable=False)
    bio = Column(Text, nullable=True)
    cv_path = Column(String(500), nullable=False)  # URL / server path to the file in cv folder
    created_at = Column(DateTime, default=datetime.utcnow)


# Aliases for convenience
UserProfile = CandidateProfile
CVProfile = CandidateProfile
