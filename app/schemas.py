from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SpotBase(BaseModel):
    latitude: float
    longitude: float
    note: Optional[str] = None
    image_url: Optional[str] = None
    place_name: Optional[str] = None
    user_id: int

class SpotCreate(SpotBase):
    pass  # Same as SpotBase for now

class SpotOut(SpotBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
# Base fields for input and output
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str] = None
    is_signed_up_for_emails: Optional[bool] = False
    role: Optional[str] = "user"

# What the client sends when registering
class UserCreate(UserBase):
    password: str  # plain password will be hashed on backend

# What the API returns (doesn't include password)
class UserOut(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True