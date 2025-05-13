from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models
from ..auth import get_current_user
from ..db import get_db

router = APIRouter()

# -----------------------------
# Follow a user
# -----------------------------
@router.post("/follow/{user_id}")
def follow_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.id == user_id:
        raise HTTPException(status_code=400, detail="You can't follow yourself.")

    target_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found.")

    if target_user in current_user.following:
        raise HTTPException(status_code=400, detail="Already following this user.")

    current_user.following.append(target_user)
    db.commit()
    return {"detail": f"You are now following {target_user.email}"}

# -----------------------------
# Unfollow a user
# -----------------------------
@router.post("/unfollow/{user_id}")
def unfollow_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    target_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found.")

    if target_user not in current_user.following:
        raise HTTPException(status_code=400, detail="You are not following this user.")

    current_user.following.remove(target_user)
    db.commit()
    return {"detail": f"You unfollowed {target_user.email}"}

# -----------------------------
# List people I follow
# -----------------------------
@router.get("/following")
def list_following(
    current_user: models.User = Depends(get_current_user)
):
    return [{"id": u.id, "email": u.email} for u in current_user.following]

# -----------------------------
# List my followers
# -----------------------------
@router.get("/followers")
def list_followers(
    current_user: models.User = Depends(get_current_user)
):
    return [{"id": u.id, "email": u.email} for u in current_user.followers]
