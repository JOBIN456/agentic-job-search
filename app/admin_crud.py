from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import User
from schema.schema import UserSchema, Userlogindata


def create_user(db: Session, user: UserSchema) -> User:
    """
    Create a new user/admin in the database.
    Raises HTTPException 400 if the username already exists.
    """
    clean_username = user.username.strip() if user.username else ""
    clean_password = user.password.strip() if user.password else ""

    existing_user = db.query(User).filter(
        User.username == clean_username
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists in DB"
        )

    new_user = User(
        username=clean_username,
        password=clean_password,
        is_staff=user.is_staff
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_all_users(db: Session) -> list:
    """
    Retrieve all users from the database.
    """
    users = db.query(User).all()
    return [
        {
            "id": user.id,
            "username": user.username,
            "is_staff": user.is_staff
        }
        for user in users
    ]


def get_user_by_id(db: Session, user_id: int) -> dict:
    """
    Retrieve a single user by ID.
    Raises HTTPException 404 if not found.
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "id": user.id,
        "username": user.username,
        "password": user.password,
        "is_staff": user.is_staff
    }


def update_user_by_id(db: Session, user_id: int, user_data: UserSchema) -> dict:
    """
    Update an existing user's username, password, or staff status.
    Raises HTTPException 404 if not found, 400 if username is already taken.
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    clean_username = user_data.username.strip() if user_data.username else ""
    clean_password = user_data.password.strip() if user_data.password else ""

    # Check if username is already taken by another user
    existing_user = db.query(User).filter(
        User.username == clean_username,
        User.id != user_id
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists in DB"
        )

    user.username = clean_username
    user.password = clean_password
    user.is_staff = user_data.is_staff

    db.commit()
    db.refresh(user)

    return {
        "message": "User updated successfully",
        "id": user.id,
        "username": user.username,
        "is_staff": user.is_staff
    }


def delete_user_by_id(db: Session, user_id: int) -> dict:
    """
    Delete a user by ID.
    Raises HTTPException 404 if not found.
    """
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


def authenticate_admin(db: Session, user_data: Userlogindata) -> User:
    """
    Verify admin credentials (username, password, and is_staff == True).
    Raises HTTPException 401 if credentials are invalid or user is not staff.
    """
    clean_username = user_data.username.strip() if user_data.username else ""
    clean_password = user_data.password.strip() if user_data.password else ""

    existing_user = db.query(User).filter(
        User.username == clean_username,
        User.password == clean_password,
        User.is_staff == True
    ).first()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    return existing_user


# Aliases for convenience
create_admin_user = create_user
get_users = get_all_users
get_user = get_user_by_id
update_user = update_user_by_id
delete_user = delete_user_by_id

