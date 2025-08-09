






from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import Genre as GenreModel, Track as TrackModel
from app.schemas.schemas import Genre, GenreCreate, Track

router = APIRouter(
    prefix="/genres",
    tags=["genres"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[Genre])
def read_genres(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    genres = db.query(GenreModel).offset(skip).limit(limit).all()
    return genres

@router.get("/{genre_id}", response_model=Genre)
def read_genre(genre_id: int, db: Session = Depends(get_db)):
    db_genre = db.query(GenreModel).filter(GenreModel.GenreId == genre_id).first()
    if db_genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    return db_genre

@router.post("/", response_model=Genre)
def create_genre(genre: GenreCreate, db: Session = Depends(get_db)):
    db_genre = GenreModel(Name=genre.Name)
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre

@router.put("/{genre_id}", response_model=Genre)
def update_genre(genre_id: int, genre: GenreCreate, db: Session = Depends(get_db)):
    db_genre = db.query(GenreModel).filter(GenreModel.GenreId == genre_id).first()
    if db_genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    
    db_genre.Name = genre.Name
    db.commit()
    db.refresh(db_genre)
    return db_genre

@router.delete("/{genre_id}", response_model=Genre)
def delete_genre(genre_id: int, db: Session = Depends(get_db)):
    db_genre = db.query(GenreModel).filter(GenreModel.GenreId == genre_id).first()
    if db_genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    
    # Check if genre has tracks
    tracks = db.query(TrackModel).filter(TrackModel.GenreId == genre_id).first()
    if tracks:
        raise HTTPException(
            status_code=400, 
            detail="Cannot delete genre with associated tracks. Update or delete tracks first."
        )
    
    db.delete(db_genre)
    db.commit()
    return db_genre

@router.get("/{genre_id}/tracks", response_model=List[Track])
def read_genre_tracks(genre_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Check if genre exists
    genre = db.query(GenreModel).filter(GenreModel.GenreId == genre_id).first()
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    
    tracks = db.query(TrackModel).filter(TrackModel.GenreId == genre_id).offset(skip).limit(limit).all()
    return tracks






