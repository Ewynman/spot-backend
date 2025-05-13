from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas
from ..db import get_db

router = APIRouter()

@router.post("/spots", response_model=schemas.SpotOut)
def create_spot(spot: schemas.SpotCreate, db: Session = Depends(get_db)):
    db_spot = models.Spot(**spot.dict())
    db.add(db_spot)
    db.commit()
    db.refresh(db_spot)
    return db_spot

@router.get("/spots", response_model=list[schemas.SpotOut])
def get_spots(db: Session = Depends(get_db)):
    return db.query(models.Spot).all()
