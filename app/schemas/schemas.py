
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

# Artist schemas
class ArtistBase(BaseModel):
    Name: str

class ArtistCreate(ArtistBase):
    pass

class Artist(ArtistBase):
    ArtistId: int

    class Config:
        from_attributes = True

# Album schemas
class AlbumBase(BaseModel):
    Title: str
    ArtistId: int

class AlbumCreate(AlbumBase):
    pass

class Album(AlbumBase):
    AlbumId: int

    class Config:
        from_attributes = True

class AlbumWithArtist(Album):
    artist: Artist

# Genre schemas
class GenreBase(BaseModel):
    Name: str

class GenreCreate(GenreBase):
    pass

class Genre(GenreBase):
    GenreId: int

    class Config:
        from_attributes = True

# MediaType schemas
class MediaTypeBase(BaseModel):
    Name: str

class MediaTypeCreate(MediaTypeBase):
    pass

class MediaType(MediaTypeBase):
    MediaTypeId: int

    class Config:
        from_attributes = True

# Track schemas
class TrackBase(BaseModel):
    Name: str
    AlbumId: Optional[int] = None
    MediaTypeId: int
    GenreId: Optional[int] = None
    Composer: Optional[str] = None
    Milliseconds: int
    Bytes: Optional[int] = None
    UnitPrice: float

class TrackCreate(TrackBase):
    pass

class Track(TrackBase):
    TrackId: int

    class Config:
        from_attributes = True

class TrackDetail(Track):
    album: Optional[Album] = None
    genre: Optional[Genre] = None
    media_type: MediaType

# Playlist schemas
class PlaylistBase(BaseModel):
    Name: str

class PlaylistCreate(PlaylistBase):
    pass

class Playlist(PlaylistBase):
    PlaylistId: int

    class Config:
        from_attributes = True

# PlaylistTrack schemas
class PlaylistTrackBase(BaseModel):
    PlaylistId: int
    TrackId: int

class PlaylistTrackCreate(PlaylistTrackBase):
    pass

class PlaylistTrack(PlaylistTrackBase):
    class Config:
        from_attributes = True

# Customer schemas
class CustomerBase(BaseModel):
    FirstName: str
    LastName: str
    Company: Optional[str] = None
    Address: Optional[str] = None
    City: Optional[str] = None
    State: Optional[str] = None
    Country: Optional[str] = None
    PostalCode: Optional[str] = None
    Phone: Optional[str] = None
    Fax: Optional[str] = None
    Email: str
    SupportRepId: Optional[int] = None

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    CustomerId: int

    class Config:
        from_attributes = True

# Employee schemas
class EmployeeBase(BaseModel):
    LastName: str
    FirstName: str
    Title: Optional[str] = None
    ReportsTo: Optional[int] = None
    BirthDate: Optional[datetime] = None
    HireDate: Optional[datetime] = None
    Address: Optional[str] = None
    City: Optional[str] = None
    State: Optional[str] = None
    Country: Optional[str] = None
    PostalCode: Optional[str] = None
    Phone: Optional[str] = None
    Fax: Optional[str] = None
    Email: Optional[str] = None

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    EmployeeId: int

    class Config:
        from_attributes = True

# Invoice schemas
class InvoiceBase(BaseModel):
    CustomerId: int
    InvoiceDate: datetime
    BillingAddress: Optional[str] = None
    BillingCity: Optional[str] = None
    BillingState: Optional[str] = None
    BillingCountry: Optional[str] = None
    BillingPostalCode: Optional[str] = None
    Total: float

class InvoiceCreate(InvoiceBase):
    pass

class Invoice(InvoiceBase):
    InvoiceId: int

    class Config:
        from_attributes = True

# InvoiceLine schemas
class InvoiceLineBase(BaseModel):
    InvoiceId: int
    TrackId: int
    UnitPrice: float
    Quantity: int

class InvoiceLineCreate(InvoiceLineBase):
    pass

class InvoiceLine(InvoiceLineBase):
    InvoiceLineId: int

    class Config:
        from_attributes = True

# Response models with relationships
class PlaylistWithTracks(Playlist):
    tracks: List[Track] = []

class InvoiceWithLines(Invoice):
    invoice_lines: List[InvoiceLine] = []
    customer: Customer

class CustomerWithInvoices(Customer):
    invoices: List[Invoice] = []
