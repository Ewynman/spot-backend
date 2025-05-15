from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .db import Base

# ----------------------------------------
# Many-to-many association for followers
# ----------------------------------------
followers = Table(
    "followers",
    Base.metadata,
    Column("follower_id", Integer, ForeignKey("users.id")),
    Column("followed_id", Integer, ForeignKey("users.id"))
)

# ----------------------------------------
# FriendRequest model
# ----------------------------------------
class FriendRequest(Base):
    __tablename__ = "friend_requests"

    id = Column(Integer, primary_key=True, index=True)
    from_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    to_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String, default="pending")  # 'pending', 'accepted', 'rejected'
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    from_user = relationship("User", foreign_keys=[from_user_id], back_populates="sent_requests")
    to_user = relationship("User", foreign_keys=[to_user_id], back_populates="received_requests")

# ----------------------------------------
# Spot model
# ----------------------------------------
class Spot(Base):
    __tablename__ = "spots"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    note = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    place_name = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="spots")

# ----------------------------------------
# User model
# ----------------------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)  # ✅ NEW
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, nullable=True)
    is_signed_up_for_emails = Column(Boolean, default=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")
    is_private = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    spots = relationship("Spot", back_populates="owner")

    following = relationship(
        "User",
        secondary=followers,
        primaryjoin=id == followers.c.follower_id,
        secondaryjoin=id == followers.c.followed_id,
        backref="followers"
    )

    sent_requests = relationship("FriendRequest", foreign_keys="[FriendRequest.from_user_id]", back_populates="from_user")
    received_requests = relationship("FriendRequest", foreign_keys="[FriendRequest.to_user_id]", back_populates="to_user")
