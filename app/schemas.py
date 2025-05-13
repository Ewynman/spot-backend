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
    first_name: str
    last_name: str
    email: str
    password: str
    phone_number: Optional[str] = None
    is_signed_up_for_emails: bool = False
    is_private: bool = False
    role: str = "user"

class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str]
    is_signed_up_for_emails: bool
    is_active: bool
    role: str
    is_private: bool
    created_at: datetime

    class Config:
        from_attributes = True
