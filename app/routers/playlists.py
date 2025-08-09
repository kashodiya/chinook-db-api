



from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import Playlist as PlaylistModel, Track as TrackModel, PlaylistTrack as PlaylistTrackModel
from app.schemas.schemas import Playlist, PlaylistCreate, PlaylistWithTracks, Track, PlaylistTrackCreate

router = APIRouter(
    prefix="/playlists",
    tags=["playlists"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[Playlist])
def read_playlists(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    playlists = db.query(PlaylistModel).offset(skip).limit(limit).all()
    return playlists

@router.get("/{playlist_id}", response_model=Playlist)
def read_playlist(playlist_id: int, db: Session = Depends(get_db)):
    db_playlist = db.query(PlaylistModel).filter(PlaylistModel.PlaylistId == playlist_id).first()
    if db_playlist is None:
        raise HTTPException(status_code=404, detail="Playlist not found")
    return db_playlist

@router.post("/", response_model=Playlist)
def create_playlist(playlist: PlaylistCreate, db: Session = Depends(get_db)):
    db_playlist = PlaylistModel(Name=playlist.Name)
    db.add(db_playlist)
    db.commit()
    db.refresh(db_playlist)
    return db_playlist

@router.put("/{playlist_id}", response_model=Playlist)
def update_playlist(playlist_id: int, playlist: PlaylistCreate, db: Session = Depends(get_db)):
    db_playlist = db.query(PlaylistModel).filter(PlaylistModel.PlaylistId == playlist_id).first()
    if db_playlist is None:
        raise HTTPException(status_code=404, detail="Playlist not found")
    
    db_playlist.Name = playlist.Name
    db.commit()
    db.refresh(db_playlist)
    return db_playlist

@router.delete("/{playlist_id}", response_model=Playlist)
def delete_playlist(playlist_id: int, db: Session = Depends(get_db)):
    db_playlist = db.query(PlaylistModel).filter(PlaylistModel.PlaylistId == playlist_id).first()
    if db_playlist is None:
        raise HTTPException(status_code=404, detail="Playlist not found")
    
    db.delete(db_playlist)
    db.commit()
    return db_playlist

@router.get("/{playlist_id}/tracks", response_model=List[Track])
def read_playlist_tracks(playlist_id: int, db: Session = Depends(get_db)):
    # Check if playlist exists
    playlist = db.query(PlaylistModel).filter(PlaylistModel.PlaylistId == playlist_id).first()
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    
    # Get all tracks in the playlist
    tracks = db.query(TrackModel).join(
        PlaylistTrackModel, 
        PlaylistTrackModel.TrackId == TrackModel.TrackId
    ).filter(
        PlaylistTrackModel.PlaylistId == playlist_id
    ).all()
    
    return tracks

@router.post("/{playlist_id}/tracks", response_model=dict)
def add_track_to_playlist(playlist_id: int, track_id: int, db: Session = Depends(get_db)):
    # Check if playlist exists
    playlist = db.query(PlaylistModel).filter(PlaylistModel.PlaylistId == playlist_id).first()
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    
    # Check if track exists
    track = db.query(TrackModel).filter(TrackModel.TrackId == track_id).first()
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    
    # Check if track is already in playlist
    existing = db.query(PlaylistTrackModel).filter(
        PlaylistTrackModel.PlaylistId == playlist_id,
        PlaylistTrackModel.TrackId == track_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Track already in playlist")
    
    # Add track to playlist
    playlist_track = PlaylistTrackModel(PlaylistId=playlist_id, TrackId=track_id)
    db.add(playlist_track)
    db.commit()
    
    return {"message": "Track added to playlist successfully"}

@router.delete("/{playlist_id}/tracks/{track_id}", response_model=dict)
def remove_track_from_playlist(playlist_id: int, track_id: int, db: Session = Depends(get_db)):
    # Check if playlist exists
    playlist = db.query(PlaylistModel).filter(PlaylistModel.PlaylistId == playlist_id).first()
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    
    # Check if track exists
    track = db.query(TrackModel).filter(TrackModel.TrackId == track_id).first()
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    
    # Check if track is in playlist
    playlist_track = db.query(PlaylistTrackModel).filter(
        PlaylistTrackModel.PlaylistId == playlist_id,
        PlaylistTrackModel.TrackId == track_id
    ).first()
    
    if not playlist_track:
        raise HTTPException(status_code=404, detail="Track not in playlist")
    
    # Remove track from playlist
    db.delete(playlist_track)
    db.commit()
    
    return {"message": "Track removed from playlist successfully"}



