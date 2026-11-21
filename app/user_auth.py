from sqlalchemy.orm import Session
from models import User
from fastapi import  Request, HTTPException, Depends
from database import get_db


def require_user(
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
        User.id == user_id
    ).first()

    if not user:
        request.session.clear()
        raise HTTPException(
            status_code=401,
            detail="User not found. Please log in again"
        )

    return user