from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SpotBase(BaseModel):
    latitude: float
    longitude: float
    note: Optional[str] = None
    image_url: Optional[str] = None
    place_name: Optional[str] = None

class SpotCreate(SpotBase):
    user_id: int

class SpotOut(SpotBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    phone_number: str | None = None
    is_signed_up_for_emails: bool = False
    role: str = "user"
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    is_private: bool

    class Config:
        from_attributes = True
