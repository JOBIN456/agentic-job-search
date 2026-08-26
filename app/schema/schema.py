from pydantic import BaseModel

class UserSchema(BaseModel):
    id: int | None = None
    username: str
    password: str
    is_staff: bool = False

    class Config:
        from_attributes = True