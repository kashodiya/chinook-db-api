

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import Track as TrackModel, Album as AlbumModel, Genre as GenreModel, MediaType as MediaTypeModel
from app.schemas.schemas import Track, TrackCreate, TrackDetail

router = APIRouter(
    prefix="/tracks",
    tags=["tracks"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[Track])
def read_tracks(
    skip: int = 0, 
    limit: int = 100, 
    album_id: Optional[int] = None,
    genre_id: Optional[int] = None,
    media_type_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(TrackModel)
    
    if album_id:
        query = query.filter(TrackModel.AlbumId == album_id)
    if genre_id:
        query = query.filter(TrackModel.GenreId == genre_id)
    if media_type_id:
        query = query.filter(TrackModel.MediaTypeId == media_type_id)
    
    tracks = query.offset(skip).limit(limit).all()
    return tracks

@router.get("/{track_id}", response_model=TrackDetail)
def read_track(track_id: int, db: Session = Depends(get_db)):
    db_track = db.query(TrackModel).filter(TrackModel.TrackId == track_id).first()
    if db_track is None:
        raise HTTPException(status_code=404, detail="Track not found")
    return db_track

@router.post("/", response_model=Track)
def create_track(track: TrackCreate, db: Session = Depends(get_db)):
    # Validate foreign keys
    if track.AlbumId:
        album = db.query(AlbumModel).filter(AlbumModel.AlbumId == track.AlbumId).first()
        if not album:
            raise HTTPException(status_code=404, detail="Album not found")
    
    if track.GenreId:
        genre = db.query(GenreModel).filter(GenreModel.GenreId == track.GenreId).first()
        if not genre:
            raise HTTPException(status_code=404, detail="Genre not found")
    
    media_type = db.query(MediaTypeModel).filter(MediaTypeModel.MediaTypeId == track.MediaTypeId).first()
    if not media_type:
        raise HTTPException(status_code=404, detail="MediaType not found")
    
    db_track = TrackModel(
        Name=track.Name,
        AlbumId=track.AlbumId,
        MediaTypeId=track.MediaTypeId,
        GenreId=track.GenreId,
        Composer=track.Composer,
        Milliseconds=track.Milliseconds,
        Bytes=track.Bytes,
        UnitPrice=track.UnitPrice
    )
    db.add(db_track)
    db.commit()
    db.refresh(db_track)
    return db_track

@router.put("/{track_id}", response_model=Track)
def update_track(track_id: int, track: TrackCreate, db: Session = Depends(get_db)):
    db_track = db.query(TrackModel).filter(TrackModel.TrackId == track_id).first()
    if db_track is None:
        raise HTTPException(status_code=404, detail="Track not found")
    
    # Validate foreign keys
    if track.AlbumId:
        album = db.query(AlbumModel).filter(AlbumModel.AlbumId == track.AlbumId).first()
        if not album:
            raise HTTPException(status_code=404, detail="Album not found")
    
    if track.GenreId:
        genre = db.query(GenreModel).filter(GenreModel.GenreId == track.GenreId).first()
        if not genre:
            raise HTTPException(status_code=404, detail="Genre not found")
    
    media_type = db.query(MediaTypeModel).filter(MediaTypeModel.MediaTypeId == track.MediaTypeId).first()
    if not media_type:
        raise HTTPException(status_code=404, detail="MediaType not found")
    
    # Update track attributes
    for key, value in track.model_dump().items():
        setattr(db_track, key, value)
    
    db.commit()
    db.refresh(db_track)
    return db_track

@router.delete("/{track_id}", response_model=Track)
def delete_track(track_id: int, db: Session = Depends(get_db)):
    db_track = db.query(TrackModel).filter(TrackModel.TrackId == track_id).first()
    if db_track is None:
        raise HTTPException(status_code=404, detail="Track not found")
    
    db.delete(db_track)
    db.commit()
    return db_track

@router.get("/search/", response_model=List[Track])
def search_tracks(
    query: str = Query(..., min_length=1, description="Search query for track name or composer"),
    db: Session = Depends(get_db)
):
    tracks = db.query(TrackModel).filter(
        (TrackModel.Name.like(f"%{query}%")) | 
        (TrackModel.Composer.like(f"%{query}%"))
    ).all()
    return tracks

