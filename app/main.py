










from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from app.routers import artists, albums, tracks, customers, employees, invoices, playlists, genres, media_types

app = FastAPI(
    title="Chinook API",
    description="API for the Chinook digital media store",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(artists.router)
app.include_router(albums.router)
app.include_router(tracks.router)
app.include_router(customers.router)
app.include_router(employees.router)
app.include_router(invoices.router)
app.include_router(playlists.router)
app.include_router(genres.router)
app.include_router(media_types.router)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def read_root():
    return RedirectResponse(url="/static/index.html")

@app.get("/api")
def read_api_info():
    return {
        "message": "Welcome to the Chinook API",
        "documentation": "/docs",
        "endpoints": [
            "/artists",
            "/albums",
            "/tracks",
            "/customers",
            "/employees",
            "/invoices",
            "/playlists",
            "/genres",
            "/media-types"
        ]
    }










