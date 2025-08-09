








from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import MediaType as MediaTypeModel, Track as TrackModel
from app.schemas.schemas import MediaType, MediaTypeCreate, Track

router = APIRouter(
    prefix="/media-types",
    tags=["media-types"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[MediaType])
def read_media_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    media_types = db.query(MediaTypeModel).offset(skip).limit(limit).all()
    return media_types

@router.get("/{media_type_id}", response_model=MediaType)
def read_media_type(media_type_id: int, db: Session = Depends(get_db)):
    db_media_type = db.query(MediaTypeModel).filter(MediaTypeModel.MediaTypeId == media_type_id).first()
    if db_media_type is None:
        raise HTTPException(status_code=404, detail="MediaType not found")
    return db_media_type

@router.post("/", response_model=MediaType)
def create_media_type(media_type: MediaTypeCreate, db: Session = Depends(get_db)):
    db_media_type = MediaTypeModel(Name=media_type.Name)
    db.add(db_media_type)
    db.commit()
    db.refresh(db_media_type)
    return db_media_type

@router.put("/{media_type_id}", response_model=MediaType)
def update_media_type(media_type_id: int, media_type: MediaTypeCreate, db: Session = Depends(get_db)):
    db_media_type = db.query(MediaTypeModel).filter(MediaTypeModel.MediaTypeId == media_type_id).first()
    if db_media_type is None:
        raise HTTPException(status_code=404, detail="MediaType not found")
    
    db_media_type.Name = media_type.Name
    db.commit()
    db.refresh(db_media_type)
    return db_media_type

@router.delete("/{media_type_id}", response_model=MediaType)
def delete_media_type(media_type_id: int, db: Session = Depends(get_db)):
    db_media_type = db.query(MediaTypeModel).filter(MediaTypeModel.MediaTypeId == media_type_id).first()
    if db_media_type is None:
        raise HTTPException(status_code=404, detail="MediaType not found")
    
    # Check if media type has tracks
    tracks = db.query(TrackModel).filter(TrackModel.MediaTypeId == media_type_id).first()
    if tracks:
        raise HTTPException(
            status_code=400, 
            detail="Cannot delete media type with associated tracks. Update or delete tracks first."
        )
    
    db.delete(db_media_type)
    db.commit()
    return db_media_type

@router.get("/{media_type_id}/tracks", response_model=List[Track])
def read_media_type_tracks(media_type_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Check if media type exists
    media_type = db.query(MediaTypeModel).filter(MediaTypeModel.MediaTypeId == media_type_id).first()
    if not media_type:
        raise HTTPException(status_code=404, detail="MediaType not found")
    
    tracks = db.query(TrackModel).filter(TrackModel.MediaTypeId == media_type_id).offset(skip).limit(limit).all()
    return tracks








