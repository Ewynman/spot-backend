from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..db import get_db
from ..auth import get_current_user

router = APIRouter()

# -----------------------------
# Create a new spot (POST /spots)
# -----------------------------
@router.post("/spots", response_model=schemas.SpotOut)
def create_spot(
    spot: schemas.SpotCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)  # 👈 Require auth
):
    # Attach the current user ID to the new spot
    db_spot = models.Spot(**spot.dict(), user_id=current_user.id)
    db.add(db_spot)
    db.commit()
    db.refresh(db_spot)
    return db_spot

# -----------------------------
# Get visible spots (GET /spots)
# -----------------------------
@router.get("/spots", response_model=list[schemas.SpotOut])
def get_visible_spots(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # 👇 Get IDs of users that current_user is following
    followed_user_ids = db.query(models.Follower.followed_id).filter(
        models.Follower.follower_id == current_user.id
    )

    # 👇 Query spots:
    spots = db.query(models.Spot).join(models.User).filter(
        (
            (models.User.is_private == False) |  # Public user
            (models.Spot.user_id == current_user.id) |  # Own spots
            (models.Spot.user_id.in_(followed_user_ids))  # From followed users
        )
    ).all()

    return spots
