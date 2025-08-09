

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import Album as AlbumModel, Artist as ArtistModel
from app.schemas.schemas import Album, AlbumCreate, AlbumWithArtist

router = APIRouter(
    prefix="/albums",
    tags=["albums"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[Album])
def read_albums(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    albums = db.query(AlbumModel).offset(skip).limit(limit).all()
    return albums

@router.get("/{album_id}", response_model=AlbumWithArtist)
def read_album(album_id: int, db: Session = Depends(get_db)):
    db_album = db.query(AlbumModel).filter(AlbumModel.AlbumId == album_id).first()
    if db_album is None:
        raise HTTPException(status_code=404, detail="Album not found")
    return db_album

@router.post("/", response_model=Album)
def create_album(album: AlbumCreate, db: Session = Depends(get_db)):
    # Check if artist exists
    artist = db.query(ArtistModel).filter(ArtistModel.ArtistId == album.ArtistId).first()
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    
    db_album = AlbumModel(Title=album.Title, ArtistId=album.ArtistId)
    db.add(db_album)
    db.commit()
    db.refresh(db_album)
    return db_album

@router.put("/{album_id}", response_model=Album)
def update_album(album_id: int, album: AlbumCreate, db: Session = Depends(get_db)):
    db_album = db.query(AlbumModel).filter(AlbumModel.AlbumId == album_id).first()
    if db_album is None:
        raise HTTPException(status_code=404, detail="Album not found")
    
    # Check if artist exists
    artist = db.query(ArtistModel).filter(ArtistModel.ArtistId == album.ArtistId).first()
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    
    db_album.Title = album.Title
    db_album.ArtistId = album.ArtistId
    db.commit()
    db.refresh(db_album)
    return db_album

@router.delete("/{album_id}", response_model=Album)
def delete_album(album_id: int, db: Session = Depends(get_db)):
    db_album = db.query(AlbumModel).filter(AlbumModel.AlbumId == album_id).first()
    if db_album is None:
        raise HTTPException(status_code=404, detail="Album not found")
    
    db.delete(db_album)
    db.commit()
    return db_album

@router.get("/by-artist/{artist_id}", response_model=List[Album])
def read_albums_by_artist(artist_id: int, db: Session = Depends(get_db)):
    # Check if artist exists
    artist = db.query(ArtistModel).filter(ArtistModel.ArtistId == artist_id).first()
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    
    albums = db.query(AlbumModel).filter(AlbumModel.ArtistId == artist_id).all()
    return albums

