
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import Artist as ArtistModel
from app.schemas.schemas import Artist, ArtistCreate

router = APIRouter(
    prefix="/artists",
    tags=["artists"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[Artist])
def read_artists(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    artists = db.query(ArtistModel).offset(skip).limit(limit).all()
    return artists

@router.get("/{artist_id}", response_model=Artist)
def read_artist(artist_id: int, db: Session = Depends(get_db)):
    db_artist = db.query(ArtistModel).filter(ArtistModel.ArtistId == artist_id).first()
    if db_artist is None:
        raise HTTPException(status_code=404, detail="Artist not found")
    return db_artist

@router.post("/", response_model=Artist)
def create_artist(artist: ArtistCreate, db: Session = Depends(get_db)):
    db_artist = ArtistModel(Name=artist.Name)
    db.add(db_artist)
    db.commit()
    db.refresh(db_artist)
    return db_artist

@router.put("/{artist_id}", response_model=Artist)
def update_artist(artist_id: int, artist: ArtistCreate, db: Session = Depends(get_db)):
    db_artist = db.query(ArtistModel).filter(ArtistModel.ArtistId == artist_id).first()
    if db_artist is None:
        raise HTTPException(status_code=404, detail="Artist not found")
    
    db_artist.Name = artist.Name
    db.commit()
    db.refresh(db_artist)
    return db_artist

@router.delete("/{artist_id}", response_model=Artist)
def delete_artist(artist_id: int, db: Session = Depends(get_db)):
    db_artist = db.query(ArtistModel).filter(ArtistModel.ArtistId == artist_id).first()
    if db_artist is None:
        raise HTTPException(status_code=404, detail="Artist not found")
    
    db.delete(db_artist)
    db.commit()
    return db_artist
